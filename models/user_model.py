from datetime import datetime

from app import db

from werkzeug.security import generate_password_hash, check_password_hash

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class UserModel(db.Model):

    __tablename__= "users"

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50), nullable = False, unique = True)
    email = db.Column(db.String(75), nullable = False, unique = True)
    password_hash = db.Column(db.String(250), nullable = False)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    followed = db.relationship('UserModel',
                               secondary = "followers",
                               primaryjoin = followers.c.follower_id == id,
                               secondaryjoin = followers.c.followed_id == id,
                               backref = db.backref("followers", lazy = 'dynamic')
                                 )
    posts = db.relationship("PostModel", back_populates ="user", lazy="dynamic", cascade="all, delete")

    def __repr__(self):
        return f'<User: {self.username}>'

    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def from_dict(self, user_dict):
        for k, v in user_dict.items():
            if k != "password":
                setattr(self, k, v)
            else:
                setattr(self, "password_hash", generate_password_hash(v))

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_following(self, user):
        return user in self.followed
  
    def follow(self, user):
        if self.is_following(user):
            return
        self.followed.append(user)

    def unfollow(self,user):
        if not self.is_following(user):
            return
        self.followed.remove(user)

class PostModel(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = False)
    user = db.relationship('UserModel', back_populates = 'posts')

    def __repr__(self):
        return f'<Post: {self.body}>'
  
    def commit(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

