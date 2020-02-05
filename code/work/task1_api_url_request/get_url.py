# Steps Online (https://cloud.google.com/vision/docs/before-you-begin)
# Enable the Cloud Vision API.
# Set up authentication
# Set environment variable to path of downloaded .json file
## in Powershell
## $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\username\Downloads\[FILE_NAME].json"
## in Linux/Mac
### export GOOGLE_APPLICATION_CREDENTIALS="/home/user/Downloads/service-account-file.json"



import os,io
from google.cloud import vision
from google.cloud.vision import types

# Set environment and create client instance
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "react-gcv-1252c1aab7d1.json"
client = vision.ImageAnnotatorClient()
dir(client)

# Process Image

file_name = "testimage2.jpg"
image_path = os.path.join('.\images',file_name)

with io.open(image_path,'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)
response = client.web_detection(image=image)
print(response)
#web_detection = response.web_detection()

# web_detection properties:
## best_guess_labels
## full_matching_images
## pages_with_matching_images
## partial_matching_images
## visually_similar_images
## web_entities

#print(web_detection.pages_with_matching_images)
