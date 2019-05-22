import logging
from datetime import datetime, timedelta
from app import db, ma


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    pseudo = db.Column(db.String(120), nullable=True)
    password = db.Column(db.String(120), nullable=True)
    created_at = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, pseudo, password):
        self.username = username
        self.email = email
        self.pseudo = pseudo
        self.password = password
        self.created_at = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'username', 'email', 'pseudo', 'created_at')


class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(120), unique=True, nullable=True)
    expired_at = db.Column(db.DateTime, unique=True, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __init__(self, code, user_id):
        self.code = code
        self.expired_at = datetime.now()+ timedelta(hours=4)
        self.user_id = user_id


class TokenSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('code', 'user_id', 'expired_at')


class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(256),  nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    video_id = db.Column(db.Integer, nullable=False)

    def __init__(self, body, user_id, video_id):
        self.body = body
        self.video_id = video_id
        self.user_id = user_id


class CommentSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'body', 'user_id', 'video_id')


class Video(db.Model):
    __tablename__ = 'video'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45),  nullable=False)
    duration = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
    source = db.Column(db.String(45), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    view = db.Column(db.Integer, nullable=False)
    enabled = db.Column(db.Integer, nullable=False)

    def __init__(self, name, duration, user_id, source, view, enabled):
        self.name = name
        self.duration = duration
        self.user_id = user_id
        self.source = source
        self.created_at = datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
        self.view = view
        self.enabled = enabled


class VideoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'name', 'duration,', 'user_id', 'source', 'created_at', 'view', 'enabled')


class Video_Format(db.Model):
    __tablename__ = 'video_format'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(128),  nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    uri = db.Column(db.String(128), nullable=False)

    def __init__(self, code, user_id, uri):
        self.code = code
        self.uri = uri
        self.user_id = user_id


class Video_FormatSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('id', 'code', 'user_id', 'uri')