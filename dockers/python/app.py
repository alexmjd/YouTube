import user
import comment
import video
import upload
import os
import logging
from flask import Flask, flash, request, redirect, url_for, make_response, jsonify, send_from_directory
from flask_jwt_extended import JWTManager
from flask_jsonpify import jsonify
from flask_restful import Resource, Api
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
api = Api(app)

# conf pour les vidéos
UPLOAD_FOLDER = '/home/videos'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
ALLOWED_EXTENSIONS = set(['webm', 'mkv', 'flv', 'avi', 'mpg','mpeg', 'mov', 'wmv', 'mp4', 'm4p'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'Not found'}), 404)


# partie user
api.add_resource(user.GetUsers, '/users')
api.add_resource(user.UserById, '/user/<user_id>')
api.add_resource(user.CreateUser, '/user')
api.add_resource(user.Authentification, '/auth')

# Partie commentaires
api.add_resource(comment.GetComments, '/video/<video_id>/comments')

# Partie vidéo
api.add_resource(video.GetVideos, '/videos')
api.add_resource(video.GetVideoById, '/video/<video_id>')
api.add_resource(video.GetVideosByIdUser, '/user/<user_id>/videos')
api.add_resource(video.CreateVideo, '/user/<user_id>/video')

# zone upload
def allowed_file(file_name):
    logging.warning("in allow func\n {}".format(file_name))
    return '.' in file_name and file_name.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        #return make_response("post is ok")
        # check if file is in the post method
        if 'test' not in request.files:
            logging.warning(request.files)
            flash('No file')
            return redirect(request.url)
        
        file = request.files['test']

        if file.filename == '':
            logging.warning("no filename")
            flash('No selected file')
            return redirect(request.url)

        logging.warning("Testing allowed file\n")
        if file and allowed_file(file.filename):
            #return "file is ok"
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.mkdir(UPLOAD_FOLDER)
                logging.warning("{} has been created\n".format(UPLOAD_FOLDER))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))
        else:
            return make_response(jsonify({'Message':'something went wrong'}))
        return make_response("ok")

@app.route('/upload/<filename>', methods=['GET'])
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)