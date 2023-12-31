import cv2
import numpy as np

import streamlit as st

import torch
import torch.nn as nn
from torchvision import models,transforms
from efficientnet_pytorch import EfficientNet

class Config:
    DIR='./src/models'

class ModelScript:
    def __init__(self,model_name):
        self.model_name=model_name
        self.model_path=f'{Config.DIR}/{self.model_name}.pt'
        self.input_shape=(128,128)

    @st.cache_resource   
    def Net(model_name='b3',output=2):
        model=EfficientNet.from_pretrained(f'efficientnet-{model_name}') 
        model._fc=nn.Linear(in_features=model._fc.in_features,out_features=output,bias=True) 
        return model
    
    def load_model(self):
        model=ModelScript.Net()
        model.load_state_dict(torch.load(self.model_path,map_location=torch.device('cpu'))["model_state_dict"])
        model.eval()
        return model

    def preprocessing(self,image):
        jpg_as_np=np.frombuffer(image,dtype=np.uint8)
        image=cv2.imdecode(jpg_as_np,cv2.IMREAD_COLOR) 
        image=torch.from_numpy(image).to(torch.float32)
        image=image.permute(2,1,0)
        transform=transforms.Compose([transforms.Resize(self.input_shape)])
        image=transform(image)
        return image

    def predict(self,image,model):
        image=image.unsqueeze(0)
        pred=model(image)
        pred=nn.functional.softmax(pred,dim=1).data.cpu().numpy().argmax()
        return pred        



