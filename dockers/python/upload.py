import os
import logging
from app import app
from flask import Flask, flash, request, redirect, url_for, make_response, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_jsonpify import jsonify
from flask_restful import Resource


UPLOAD_FOLDER = '/home/videos'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#ALLOWED_EXTENSIONS = set(['webm', 'mkv', 'flv', 'avi', 'mpg','mpeg', 'mov', 'wmv', 'mp4', 'm4p'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class Upload(Resource):
    def allowed_file(self, file_name):
        logging.warning("in allow func\n {}".format(file_name))
        return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    def upload_file(self):
        #return "ok"
        logging.warning("Good route 1\n")
        if request.method == 'POST':
            #return make_response("post is ok")
            # check if file is in the post method
            if 'source' not in request.files:
                logging.warning(request.files)
                return "no file"
                flash('No file')
                return redirect(request.url)
            
            file = request.files['source']

            if file.filename == '':
                logging.warning("no filename")
                return "no filename"
                flash('No selected file')
                return redirect(request.url)

            logging.warning("Testing allowed file\n")
            if file and self.allowed_file(file.filename):
                logging.warning("Good route 2\n")
                #return "file is ok"
                filename = secure_filename(file.filename)
                if not os.path.exists(UPLOAD_FOLDER):
                    os.mkdir(UPLOAD_FOLDER)
                    logging.warning("{} has been created\n".format(UPLOAD_FOLDER))
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return filename
                #return redirect(url_for('uploaded_file', filename=filename))
            else:
                logging.warning(file)
                logging.warning(self.allowed_file(file.filename))
                return make_response(jsonify({'Message':'something went wrong'}))
            return make_response("ok")

    def uploaded_file(filename):
        logging.warning("Good route 4\n")
        return send_from_directory(app.config['UPLOAD_FOLDER'],filename)
