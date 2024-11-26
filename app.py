from . import app, db
from flask import request, make_response
from .models import Users, Locations, BlogPosts
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

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
        return make_response({'token': token}, 201)
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


# @app.route("/blog", methods=["POST"])
# @token_required
# @cross_origin
# def get_user_blog_posts(current_user):
#     blog_posts = BlogPosts.query.filter_by(posted_by=current_user.id).all()
#     number_blog_posts = 0
#     if blog_posts:
#         number_blog_posts = len(blog_posts)
#     return make_response({
#         "data": [text["user_text"] for text in blog_posts],
#         "number": number_blog_posts
#     })


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
        return make_response("Could not get location data.", 500)
    


@app.route("/blog/<id>", methods=["GET"])
@token_required
def get_blog_posts(id):
    blog_posts = BlogPosts.query.filter_by(location_id=id).all()
    data = []
    for post in blog_posts:
        data.append({"id": post.id,
                     "created_at": post.created_at,
                     "posted_by": post.posted_by,
                     "user_text": post.user_text,
                     "is_reply": post.is_reply,
                     "reply_to": post.reply_to,
                     "likes": post.likes})
    if blog_posts:
        return make_response(data, 200)
    else:
        return make_response("Could not get blog data.", 500)