def Analyze_sentiment(content):
    from google.cloud import language_v1
    from google.cloud.language_v1 import enums
    import six
    import os,glob
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\parth_rastogi2394\\Desktop\\Hackathon\\hackathon-234211-d2af5b95d530.json'

    client = language_v1.LanguageServiceClient()
    
    if isinstance(content, six.binary_type):
        content = content.decode('utf-8')

    type_ = enums.Document.Type.PLAIN_TEXT
    document = {'type': type_, 'content': content}

    response = client.analyze_sentiment(document)
    sentiment = response.document_sentiment
    if -1 <= sentiment.score <= -0.25:
        print('The document has \t Negative Sentiment')
    if -0.25 < sentiment.score < 0.25:
        print('The document has \t Neutral Sentiment')
    if 0.25 <= sentiment.score < 1:
        print('The document has \t Positive Sentiment')


    
