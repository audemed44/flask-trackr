from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    lists = db.relationship('Lists', backref='author', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Lists(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    media = db.Column(db.String(7))
    media_id = db.Column(db.Integer)
    user_score = db.Column(db.String(4))
    status = db.Column(db.String(25))

    def __repr__(self):
        return '<List {} {} {} {}>'.format(self.user_id,self.media_id, self.user_score, self.media)


class TopAnime(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rank = db.Column(db.Integer)
    mal_id = db.Column(db.Integer, index=True, unique=True)
    title = db.Column(db.String(128))
    image_url = db.Column(db.String(256))
    episodes = db.Column(db.Integer)
    mal_score = db.Column(db.String(4))

    def __repr__(self):
        return '<Top Anime {} {} {}'.format(self.rank,self.title,self.mal_score)

class Anime(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rank = db.Column(db.Integer)
    mal_id = db.Column(db.Integer, index=True, unique=True)
    title = db.Column(db.String(128))
    image_url = db.Column(db.String(256))
    episodes = db.Column(db.Integer)
    mal_score = db.Column(db.String(4))
    synopsis = db.Column(db.Text())

    def __repr__(self):
        return '<Anime {} {} {}'.format(self.rank, self.title, self.mal_score)


class MAL_Database(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    rank = db.Column(db.Integer)
    mal_id = db.Column(db.Integer, index=True, unique=True)
    title = db.Column(db.String(128))
    anime_type = db.Column(db.String(20))
    start_date = db.Column(db.String(50))
    end_date = db.Column(db.String(50))
    image_url = db.Column(db.String(256), index=True)
    mal_url = db.Column(db.String(256))
    episodes = db.Column(db.Integer)
    mal_score = db.Column(db.String(4))
    members = db.Column(db.Integer)

    def __repr__(self):
        return 'DB: ID-{} Rank-{} Title-{} Episodes-{}'.format(self.mal_id,self.rank,self.title,self.episodes)
    
