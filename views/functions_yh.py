import subprocess, json
import models.transcriptor as transcriptor
from models.trainedmodel import predict_text
from models.yhdatamodel import DataModel, FailureResponse, FLAGREASONS

def isfraud(text):
    isFraud, prob = predict_text(text)
    return isFraud, prob

def checkfiletype(string):
    if string.split('/')[0] in ['video', 'audio']:
        return True
    else:
        return False


def check_audio_length(filename):
    result = subprocess.check_output(
        f'ffprobe -v quiet -show_streams -select_streams a:0 -of json "{filename}"',
        shell=True).decode()
    fields = json.loads(result)['streams'][0]
    duration = fields['duration']
    return float(duration)


def transcriptfile(tmpLocation, result, checkFraud):
    transcript = transcriptor.transcript_audio(tmpLocation)
    text = " ".join([x['text'] for x in transcript['segments']])
    result.data = DataModel(transcript=text)
    if checkFraud:
        fraudresult, prob = isfraud(text)
        result.fraudCode = fraudresult
        result.probability = prob
    result.resultCode = True

def resultflag(flag):
    result = FailureResponse(
        reasoncode=flag,
        reasondetails=FLAGREASONS[flag]
    )
    return result
