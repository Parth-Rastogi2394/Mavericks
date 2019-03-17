import spacy
import nltk
import random
from gensim import corpora
import pickle
import gensim
import re,os
from spacy.lang.en import English
from nltk.corpus import wordnet as wn
#nltk.download('wordnet')
#nltk.download('stopwords')
text_data = []
parser = English()
en_stop = set(nltk.corpus.stopwords.words('english'))

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)


def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

            
def topics(Transcript,Scripts_Path):
    Transcript_list = Transcript.split("\n")
    for line in Transcript_list:
        tokens = prepare_text_for_lda(line)
        text_data.append(tokens)
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    pickle.dump(corpus, open(os.path.join(Scripts_Path,'corpus.pkl'), 'wb'))
    dictionary.save(os.path.join(Scripts_Path,'dictionary.gensim'))

    NUM_TOPICS = 5
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
    ldamodel.save(os.path.join(Scripts_Path,'model5.gensim'))
    final_topics = []
    topics = ldamodel.print_topics(num_words=4)
    for topic in topics:
        #print(topic)
        topics_list = topic[1].split('+')
        final_topics = final_topics + [re.sub("\""," ",i.split('*')[1]).strip() for i in topics_list]

    final_topics = ','.join(list(set(final_topics)))
    return final_topics


def Find_Relevant_Topics(Transcript,Scripts_Path):
    return(topics(Transcript,Scripts_Path))
    



