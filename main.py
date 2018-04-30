import numpy as np
import cv2 as cv2
import os
from PIL import Image
from io import StringIO
import time
import boto3
from flask import Flask, request, render_template,redirect, url_for,session


app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
cam = None

@app.route("/")
def index():
    session['user_type'] = ''
    return render_template('index.html',data = '')

@app.route("/learn", methods=['POST'])
def learn():
    if request.form['password']=='cmpe297':
        session['user_type'] = 'admin'
        return render_template('learn.html', data = '')
    else:
        return render_template('index.html', data = 'Wrong Password!')



@app.route("/learn_face", methods=['POST'])
def learn_face():
    if request.method == 'POST':
        if session.get('user_type')=='admin':
            session['stop'] = None
            start = time.time()

            # Create an S3 client
            AWS_ACCESS_KEY = 'AKIAJY32U7FW46ASWYKA'
            AWS_ACCESS_SECRET_KEY = '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'
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
            runtime = 0
            while(session['stop'] is None ):
                if session.get('person') is not None:
                    cam.release()
                    cv2.destroyAllWindows()
                    return render_template('index.html',data = session.get('person'))
                runtime+=1
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
                    image.save('Learn-'+str(request.form['name'])+'-0.png')
                    milli_sec = int(round(time.time() * 1000))
                    s3.upload_file('Learn-'+str(request.form['name'])+'-0.png', 'facialrecognitionimages02', 'Learn-'+str(request.form['name'])+'-'+str(i)+str(milli_sec)+'.png',ExtraArgs={'ACL': 'public-read'})
                    i=i+1
                    break
                end = time.time()
                if (end - start) >25:
                    break






            cam.release()
            cv2.destroyAllWindows()
            return render_template('index.html',data = '')
        else:
            return render_template('index.html',data = '')
    cam.release()
    cv2.destroyAllWindows()
    return render_template('index.html',data = '')
@app.route("/find_face",methods=['POST'])
def find_face():
    session['user_type']=''
    if request.method =='POST':
        session['stop'] = None
        start = time.time()

        # Create an S3 client
        AWS_ACCESS_KEY = 'AKIAJY32U7FW46ASWYKA'
        AWS_ACCESS_SECRET_KEY = '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'
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
        runtime = 0
        while(session.get('stop') is None ):
            if session.get('person') is not None:
                cam.release()
                cv2.destroyAllWindows()
                return render_template('index.html',data = session.get('person'))
            runtime+=1
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
                milli_sec = int(round(time.time() * 1000))
                s3.upload_file('0.png', 'facialrecognitionimages02', '0.png',ExtraArgs={'ACL': 'public-read'})
                i=i+1
                break
            end = time.time()
            if (end - start) >25:
                break






        cam.release()
        cv2.destroyAllWindows()
        return render_template('index.html',data = '')
    else:
        return render_template('index.html',data = '')
    cam.release()
    cv2.destroyAllWindows()
    return render_template('index.html',data = '')


@app.route("/stop_learn", methods=['POST'])
def stop_learn():
    session['stop'] = None
    
    return render_template('index.html',data = '')

@app.route("/found_face", methods=['GET'])
def found_face():
    session['person'] = request.args['found']
    return render_template('index.html',data = '')


if __name__ == '__main__':
    #try to save to file through requests?

    app.run(host='0.0.0.0')



