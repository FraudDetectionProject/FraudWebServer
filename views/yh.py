from fastapi import APIRouter, UploadFile
from typing import Union
import os, shutil
from collections import Counter
import base64

from models.yhdatamodel import *
from .functions_yh import *

AUDIOLENGTH = 30
TMPLOCATION = 'tmp/tmpfile'
os.makedirs('tmp', exist_ok=True)

router = APIRouter(prefix='/yh/fraud')

@router.post('/transcript', response_model=Union[SuccessResponse, FailureResponse])
def transcriptaudio(file: UploadFile, checkFraud: Union[bool, None] = True):
    flag = 0
    if checkfiletype(file.content_type):

        with open(TMPLOCATION, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        if check_audio_length(TMPLOCATION) > AUDIOLENGTH:
            result = SuccessResponse()
            transcriptfile(TMPLOCATION, result, checkFraud)
            return result
        else:
            flag = 1
    else:
        flag = 2
    return resultflag(flag)

@router.post('/transcriptjson', response_model=Union[SuccessResponse, FailureResponse])
def transcriptaudiojson(file: FileasJSON):
    base64byte = str.encode(file.file)
    realfile = base64.b64decode(base64byte)
    flag = 0
    with open(TMPLOCATION, 'wb') as f:
        f.write(realfile)
    try:
        duration = check_audio_length(TMPLOCATION)
        if duration > AUDIOLENGTH:
            result = SuccessResponse()
            transcriptfile(TMPLOCATION, result, file.checkfraud)
            return result
        else:
            flag = 1
    except:
        flag = 2
    return resultflag(flag)