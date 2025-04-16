from . import app, db
from flask import request, make_response
# from flask_cors import CORS
from .models import Users, Locations, BlogPosts
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

# CORS(app)

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    f_name = data.get("f_name")
    l_name = data.get("l_name")
    user_name = data.get("user_name")
    password = data.get("password")

    if f_name and l_name and email and user_name:
        user = Users.query.filter_by(email=email).first()
        if user:
            return make_response(
                {"message": "A user already exists with that email."},
                200
            )
        user = Users(
            email = email,
            password = generate_password_hash(password),
            f_name = f_name,
            l_name = l_name,
            user_name = user_name
        )
        db.session.add(user)
        db.session.commit()
        return make_response(
            {
                "message": "User created."
            }, 201
        )
    return make_response(
        {
            "message": "Unable to create new user."
        }, 500
        )

@app.route("/login", methods=["POST"])
def login():
    auth = request.json
    if not auth or not auth.get("email") or not auth.get("password"):
        return make_response("Invalid email or password.", 401)
    
    user = Users.query.filter_by(email = auth.get("email")).first()
    if not user:
        return make_response("Please create an account", 401)
    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.now() + timedelta(minutes=60)
        },
        "secret",
        "HS256")
        return make_response({'token': token, 'user': {'id': user.id, 'name': user.user_name}}, 201)
    return make_response('Invalid credentials.', 401)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']
        if not token:
            return make_response({"message": "Token is missing"}, 401)
        
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
            print(current_user)
        except Exception as e:
            print(e)
            return make_response({
                "message": "Token is invalid"
            }, 401)
        return f(current_user, *args, **kwargs)
    return decorated


@app.route("/locations", methods=["GET"])
def get_locations():
    locations = Locations.query.all()
    data = []
    for loc in locations:
        data.append({"lat": loc.latitude,
                     "long": loc.longitude,
                     "_id": loc.id})
    if locations:
        return make_response(data, 200)
    else:
        return make_response("Failed to get locations.", 500)


@token_required
@app.route("/blog/<int:id>", methods=["GET"])
def get_blog_posts(id):
    blog_posts = BlogPosts.query.filter_by(location_id=id).order_by(BlogPosts.created_at.desc()).all()
    data = []
    for post in blog_posts:
        likes = len(post.likers)
        data.append({"id": post.id,
                     "created_at": post.created_at,
                     "posted_by": post.posted_by,
                     "user_text": post.user_text,
                     "is_reply": post.is_reply,
                     "reply_to": post.reply_to,
                     "likes_count": post.likes_count,
                     "user_name": post.user.user_name,
                     "likers": likes})
    if blog_posts:
        return make_response(data, 200)
    else:
        return make_response("Could not get blog data.", 500)


@token_required
@app.route("/blog", methods=["POST"])
def add_new_blog_posts():
    data = request.get_json()
    new_post = BlogPosts(location_id=data.get('location_id'),
                         posted_by=data.get('posted_by'),
                         user_text=data.get('user_text'),
                         is_reply=data.get('is_reply'),
                         reply_to=data.get('reply_to'),
                         likes_count=data.get('likes_count'),
                         )
    db.session.add(new_post)
    db.session.commit()
    return make_response('Post added successfully!', 201)


@token_required
@app.route('/like/<int:id>', methods=['POST'])
def like(id):
    user_id = request.get_json()
    user = Users.query.get_or_404(user_id['user_id'])
    post = BlogPosts.query.get_or_404(id)
    
    liked = user.like_post(post)
    if liked:
        return make_response('Post liked successfully!', 201)
    else:
        return make_response('Post unliked', 202)
