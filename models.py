from . import app, db
import location_data from dml
from sqlalchemy import func

likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('blogpost_id', db.Integer, db.ForeignKey('blogposts.id'), primary_key=True),
)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(500), nullable=False)
    f_name = db.Column(db.String(15), nullable=False)
    l_name = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    blog_posts = db.relationship('BlogPosts', backref='user', lazy=True)

    liked_posts = db.relationship('BlogPosts', secondary=likes, back_populates='likers')

    def __repr__(self):
        return f'<User {self.user_name} id: {self.id}'

    def like_post(self, post):
        """Add a like to a blog post."""
        if post not in self.liked_posts:
            self.liked_posts.append(post)
            db.session.commit()
            return True
        else:
            self.liked_posts.remove(post)
            db.session.commit()
            return False

    def unlike_post(self, post):
        """Remove a like from a blog post."""
        if post in self.liked_posts:
            self.liked_posts.remove(post)
            db.session.commit()

    
class Locations(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(15), nullable=False)
    longitude = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    blog_posts = db.relationship('BlogPosts', backref='locations', lazy=True)


class BlogPosts(db.Model):
    __tablename__ = 'blogposts'
    id = db.Column(db.Integer, primary_key=True)
    posted_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    location_id = db.Column(db.Integer, db.ForeignKey("locations.id"))
    likes_count = db.Column(db.Integer)
    user_text = db.Column(db.Text)
    is_reply = db.Column(db.Boolean)
    reply_to = db.Column(db.Integer)

    # Relationship to Users via the 'likes' table
    likers = db.relationship('Users', secondary=likes, back_populates='liked_posts')


with app.app_context():
    db.create_all()
    for coord in location_data:
        location = Locations(latitude=coord[0], longitude=coord[1])
        db.session.add(location)
    db.session.commit()