from flask import Flask, request
import torch
from PIL import Image
from torchvision import transforms
import requests
import wget
import os
from collections import OrderedDict

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

model = torch.hub.load('pytorch/vision:v0.9.0', 'densenet121', pretrained=True)
model.eval()

@app.route("/upload", methods=["GET"])
def classify_image():
   image = request.args.get('image')
   input_image = read_image(image)
   preprocess = transforms.Compose([
      transforms.Resize(256),
      transforms.CenterCrop(224),
      transforms.ToTensor(),
      transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
   ])
   input_tensor = preprocess(input_image)
   input_batch = input_tensor.unsqueeze(0)

   if torch.cuda.is_available():
      input_batch = input_batch.to('cuda')
      model.to('cuda')

   with torch.no_grad():
      output = model(input_batch)

   probabilities = torch.nn.functional.softmax(output[0], dim=0)

   url = 'https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt'
   wget.download(url, '')
   # Read the categories
   with open("imagenet_classes.txt", "r") as f:
       categories = [s.strip() for s in f.readlines()]
   # Show top categories per image
   top5_prob, top5_catid = torch.topk(probabilities, 5)
   result = OrderedDict()
   for i in range(top5_prob.size(0)):
      result[str(top5_prob[i].item())] = categories[top5_catid[i]].upper()
   os.remove("imagenet_classes.txt")

   return result

def read_image(image):
   file = './image/'+image
   try:
      user_image = Image.open(file)
   except FileNotFoundError:
      user_image = Image.open(requests.get(image, stream=True).raw)

   return user_image.convert('RGB')

if __name__ == '__main__':
   app.run(host='0.0.0.0')