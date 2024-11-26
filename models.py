from . import db
from sqlalchemy import func

class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    f_name = db.Column(db.String(15), nullable=False)
    l_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User {self.user_name} id: {self.id}'
    
class Locations(db.Model):
    __tablename__ = "Locations"
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(15), nullable=False)
    longitude = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    blog_posts = db.relationship('BlogPosts', backref="Locations")


class BlogPosts(db.Model):
    __tablename__ = "BlogPosts"
    id = db.Column(db.Integer, primary_key=True)
    posted_by = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    location_id = db.Column(db.Integer, db.ForeignKey("Locations.id"))
    likes = db.Column(db.Integer)
    user_text = db.Column(db.Text)
    is_reply = db.Column(db.Boolean)
    reply_to = db.Column(db.Integer)
