import fasttext
import re
import torch
import torch.nn as nn
import torch.optim as optim
import torch.functional as F

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
FILENAME = 'models/best_cnn_model.pt'
class CNNClassifier(nn.Module):
    def __init__(self, num_classes, in_channels, out_channels, kernel_size=1, stride=1):
        super(CNNClassifier,self).__init__()
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.kernel_size = kernel_size

        self.conv1d = nn.Conv1d(in_channels, out_channels, kernel_size)
        self.relu = nn.ReLU(inplace=True)
        self.fc1 = nn.Linear(out_channels * (out_channels - kernel_size + 1),50)
        self.fc2 = nn.Linear(50,num_classes)
        # self.softmax = nn.Softmax(dim=1)

    def forward(self,x):
        x = self.conv1d(x)
        x = self.relu(x)
        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        # x = self.softmax(x)
        return x



embedmodel = fasttext.load_model('models/model.bin')
loaded_model = CNNClassifier(2, 1, 300).to(DEVICE)
loaded_model.load_state_dict(torch.load(FILENAME))
softmax = nn.Softmax(dim=1)

### 한글 re 규칙 생성
hangul = re.compile(r'[^(가-힣| )]')

# Only fasttext
# def predict_text(text):
#     ### 한글만 추출
#     text = hangul.sub('', text)
#     prediction = model.predict(text)
#     return bool(int(prediction[0][0].split('__label__')[-1])), prediction[1][0]


# fasttext + CNN
def predict_text(sentence, model=loaded_model):
    # print(type(sentence))
    sentence = hangul.sub('', sentence)
    embedded_sentence = embedmodel.get_sentence_vector(sentence)
    embedded_tensor = torch.tensor(embedded_sentence).reshape(-1,1,300).cuda()
    predict = model(embedded_tensor)
    prepredict = softmax(predict).cpu().detach().numpy()[0]
    difference = abs(prepredict[1] - prepredict[0])
    print(prepredict)
    return predict.argmax().item(), float(difference)