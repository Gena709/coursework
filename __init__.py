from flask import Flask, request, jsonify, abort, redirect, url_for, render_template, send_file, flash, after_this_request, g

import mediapipe as mp

import numpy as np

import json

import time

import cv2

import zipfile

import threading
sem = threading.Semaphore()

app = Flask(__name__)


from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired

app.config.update(dict(
    SECRET_KEY="powerful secretkey",
    WTF_CSRF_SECRET_KEY="a csrf secret key"
))

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    file = FileField('file', validators=[DataRequired()])
    Ger = StringField('Ger', validators=[DataRequired()])

from werkzeug.utils import secure_filename
import os

ALLOWED_EXTENSIONS = set(['mp4', 'wmv', 'avi'])



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



clients = {}

@app.route("/status/<user>")
def hello_world(user):
    if user in clients:
        return clients[user]
    return ''
   

@app.route('/', methods=('GET', 'POST'))
def submit(): 
    form = MyForm() 
    if form.validate_on_submit():
        iD_status = form.Ger.data
        clients[iD_status] = "Wating for another client <br>"
        sem.acquire()
        clients[iD_status] = " Saving your file ! <br>"
        f = form.file.data
        file = request.files['file']
        print(clients)
        filename = file.filename
        if (allowed_file(filename)):
            f.save(os.path.join('', filename))
        else:
            return "<h1>There is no file or File resolution isn't good!<h1>"
        if file and allowed_file(file.filename):
            entrance = filename
            exit_video ="video_"+ filename+".mp4"
            exit_metric = "metric_" +filename + ".json"

            exit_ZIP = form.name.data + ".zip"
            mpDraw = mp.solutions.drawing_utils
            mpPose = mp.solutions.pose
            pose = mpPose.Pose()
            cap = cv2.VideoCapture(entrance)  # входящее имя
            Total = []
            forcc=cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
            out=cv2.VideoWriter(exit_video,forcc,int(cap.get(cv2.CAP_PROP_FPS)), (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))) # выходящее название вайла
            clients[iD_status] = clients[iD_status] + form.name.data + ":"+" rendering file - "+ filename + " <br>"
            # выходящее название видео файла
            while (cap.isOpened()):
                ret, img = cap.read()
                if ret == True:
                    h, w, c = img.shape
                    lmlist = [int(cap.get(cv2.CAP_PROP_POS_FRAMES)),int(cap.get(cv2.CAP_PROP_FPS)),h,w,int(cap.get(cv2.CAP_PROP_POS_FRAMES))/int(cap.get(cv2.CAP_PROP_FPS))]
                    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    results = pose.process(imgRGB)
                    if results.pose_landmarks:
                        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                        for id, lm in enumerate(results.pose_landmarks.landmark):
                            lmlist.append([id,lm.x,lm.y,lm.z,lm.visibility])
                    Total.append(lmlist)  
                    out.write(img)
                    if cv2.waitKey(1)== ord('q'):
                        break
                else:
                    break

            cap.release()
            out.release()
            
            with open(exit_metric,'w') as outfile: # выходящее название файла метрики
                json.dump(Total, outfile)

            with zipfile.ZipFile(exit_ZIP,'w') as my_zip:
                my_zip.write(exit_video)
                my_zip.write(exit_metric)
            
            os.remove(exit_video)
            os.remove(exit_metric)
            os.remove(entrance)
            clients[iD_status] = clients[iD_status] + form.name.data + ":"+" Sendng files" + " <br>"
            sem.release()
            print(clients)

            @after_this_request
            def remove_file(response):
                os.remove(exit_ZIP) 
                return response

            time.sleep(5)
            clients.pop(iD_status, None)
            return send_file(exit_ZIP, attachment_filename=exit_ZIP, as_attachment=True)
        else:
            return "<h1>error file!<h1>"
    return render_template('submit.php', form=form)

if __name__ == "__main__":
    app.run(debug = True, host = '0.0.0.0', port =5000)