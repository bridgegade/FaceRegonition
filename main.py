import numpy as np
import cv2 as cv2
import os
from PIL import Image
from io import StringIO

import boto3
# Create an S3 client
AWS_ACCESS_KEY = '***'
AWS_ACCESS_SECRET_KEY = '***'
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_ACCESS_SECRET_KEY
)

# Call S3 to list current buckets
response = s3.list_buckets()
print(response)
# Get a list of all bucket names from the response


HAR_CLAS = "haarcascade_frontalface_alt.xml"
face_cascade = cv2.CascadeClassifier(HAR_CLAS)
cam = cv2.VideoCapture(0)
i=0
while(True):
    ret, img = cam.read() # we got image
    faces = face_cascade.detectMultiScale(img, 1.6, 6)

    # now see if there are faces
    if(len(faces)!=0):

      print("Psst! "+str(len(faces))+" peep(s) at the door!")
      for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0), 2) # red box around the face
        # ... do your stuff, e.g. image sharpening, cropping, etc. ... 
        # ... I used AWS CLI to upload these images to S3
        

        #file = open('testing.txt', 'r+')

        image = Image.fromarray(img, 'RGB')
        image.save('0.png')

        s3.upload_file('0.png', 'facialrecognitionimages01', str(i)+'.png',ExtraArgs={'ACL': 'public-read'})
        i=i+1
        #s3.upload_fileobj(image, 'facialrecognitionimages', str(i))






cam.release()
cv2.destroyAllWindows()




