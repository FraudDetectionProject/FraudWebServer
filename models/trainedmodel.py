import fasttext
import re


### 한글 re 규칙 생성
hangul = re.compile(r'[^(가-힣| )]')
model = fasttext.load_model('models/model.bin')

def predict_text(text):
    ### 한글만 추출
    text = hangul.sub('', text)
    prediction = model.predict(text)
    return bool(int(prediction[0][0].split('__label__')[-1])), prediction[1][0]