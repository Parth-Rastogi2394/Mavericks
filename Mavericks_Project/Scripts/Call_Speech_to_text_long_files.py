def process(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    import os,io
    #from google.cloud import speech
    from google.cloud import speech_v1p1beta1 as speech
    from google.cloud.speech_v1p1beta1 import enums
    from google.cloud.speech_v1p1beta1 import types
    
    #from google.cloud.speech import enums
    #from google.cloud.speech import types
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'C:\\Users\\parth_rastogi2394\\Desktop\\Hackathon\\hackathon-234211-d2af5b95d530.json'

    client = speech.SpeechClient()
    first_lang = 'en-GB'
    second_lang = 'en-GB'
    third_lang='en-GB'
    audio = types.RecognitionAudio(uri=gcs_uri)
    config = speech.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=24000,
        enable_speaker_diarization = True,
        diarization_speaker_count=2,
        language_code=first_lang,
        alternative_language_codes=[second_lang,third_lang])
       
    operation = client.long_running_recognize(config, audio)
    print('Waiting for Speech-to-Text operation to complete...')
    response = operation.result(timeout=9000)
    #print(response)
    result = response.results[-1]

    words_info = result.alternatives[0].words

    tag=1
    speaker=""
    Trans = ""
    for word_info in words_info:
        if word_info.speaker_tag==tag:
            speaker=speaker+" "+word_info.word

        else:
            #print("sepaker {}: {}".format(tag,speaker))
            Trans = Trans + " "+ str(speaker)
            Trans = Trans + "\n"
            tag=word_info.speaker_tag
            speaker=""+word_info.word
            
    return Trans
            
