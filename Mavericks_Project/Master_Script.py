import os,glob
import sys
from subprocess import call
from google.cloud import storage
import pickle
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import time
cwd = os.getcwd()
Scripts_Path = os.path.join(cwd,'Scripts')
sys.path.append(Scripts_Path)
import Call_Speech_to_text_long_files
import Sentiment_analysis
import Find_topics
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\parth_rastogi2394\\Desktop\\Hackathon\\hackathon-234211-d2af5b95d530.json'

Input_Dir = os.path.join(cwd,'Inputs')

def convert_mp3(mp3_list,target_dir):
    for mp3 in mp3_list:
        flac = mp3[:-4] + ".flac"
        if os.path.isfile(flac):
            #print('File ' + flac + ' already exists')
            print('Flac Conversion Done')
        else:
            call(["ffmpeg", "-i", mp3, flac])
            print('Flac Conversion Done')

def upload_flac_files(Flac_Files):

    for Each_Flac in Flac_Files:
        Flac_FileName = os.path.basename(Each_Flac)
        print('File under Process \t',Flac_FileName)
        storage_client = storage.Client()
        buckets = list(storage_client.list_buckets())

        bucket = storage_client.get_bucket("hackathon-mavericks")
        blob = bucket.blob(Flac_FileName)
        blob.upload_from_filename(Each_Flac)
        #print(buckets)
        
def Make_Topic_TDM(Topics):
    Bag_of_words_file = open(os.path.join(Scripts_Path,'Bag_of_words.txt'),'r')
    Bag_of_words_text = Bag_of_words_file.read()
    Bag_of_words = Bag_of_words_text.split("\t")
    Topic_list = [i if i in Bag_of_words else '' for i in Topics.split(',')]
    Value_for_topics = [1 if i in Topic_list else 0 for i in Bag_of_words]
    tdm_df = pd.DataFrame(columns=Bag_of_words)
    tdm_df.loc[1] = Value_for_topics
    return tdm_df

def Topic_of_Document(Topic_TDM):
    Prediction_of_topic = pickle.load(open(os.path.join(Scripts_Path,"Predict_Topic.pickle"), 'rb'))
    Topic_Predicted = Prediction_of_topic.predict(Topic_TDM)
    return Topic_Predicted

if __name__ == '__main__':
    All_Mp3_Files = glob.glob(os.path.join(Input_Dir,"*.mp3"))
    convert_mp3(All_Mp3_Files,Input_Dir)
    Flac_Files = glob.glob(os.path.join(Input_Dir,"*.flac"))
    upload_flac_files(Flac_Files)
    for Each_Flac in Flac_Files:
        Flac_file = "gs://hackathon-mavericks/"+os.path.basename(Each_Flac)
        Transcript = Call_Speech_to_text_long_files.process(Flac_file)
        print("################################")
        Sentiment_analysis.Analyze_sentiment(Transcript)
        Topics = Find_topics.Find_Relevant_Topics(Transcript,Scripts_Path)
        Topic_TDM = Make_Topic_TDM(Topics)
        Predicted_Topic = Topic_of_Document(Topic_TDM)
        print("################# Topic Predicted ##################")
        if len(Predicted_Topic) > 0 :
            print(Predicted_Topic)
        else:
            print("Prediction Failed")
    time.sleep(900)
        
    
