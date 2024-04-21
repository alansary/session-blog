from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_restful import Api, Resource, reqparse
from werkzeug.exceptions import BadRequest
from flask import make_response, jsonify
import datetime
from flask import render_template

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # SQLite database
db = SQLAlchemy(app)

class PostModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True, nullable=False)
    text = db.Column(db.Text(), nullable=True)
    images = db.Column(db.JSON(), nullable=True)
    video_link = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime(), nullable=False)
    updated_at = db.Column(db.DateTime(), nullable=True)

    def __repr__(self):
        return f"Post(title={self.title})"

    def as_dict(self):
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }

if os.path.exists('instance/database.db'):
    print('Database already exists')
else:
    with app.app_context():
        db.create_all()
    print('Database created successfully')

class Posts(Resource):
    def post(self):
        posts_post_args = reqparse.RequestParser()
        posts_post_args.add_argument(
            "title", type=str, required=True, help="Post title is required"
        )
        posts_post_args.add_argument("text", type=str, required=False)
        posts_post_args.add_argument(
            "images", type=str, required=False, action="append"
        )
        posts_post_args.add_argument("video_link", type=str, required=False)

        try:
            args = posts_post_args.parse_args() # to validate the request arguments
            try:
                post = PostModel(
                    title=args['title'],
                    text=args['text'],
                    images=args['images'],
                    video_link=args['video_link'],
                    created_at=datetime.datetime.now()
                )
                db.session.add(post)
                db.session.commit()

                return make_response(jsonify(post.as_dict()), 201)
            except Exception as e:
                return make_response(jsonify({"error": f"An error occurred: {e._message}"}), 500)
        except BadRequest as e:
            return make_response(jsonify({"error": e.description}), e.code)

    def get(self):
        posts = PostModel.query.all()
        posts_as_json = [post.as_dict() for post in posts]
        return make_response(jsonify(posts_as_json), 200)

class Post(Resource):
    def get(self, post_id):
        post = PostModel.query.filter_by(id=post_id).first()
        if not post:
            return make_response(jsonify({"error": f"Post with ID {post_id} not found"}), 404)
        return make_response(jsonify(post.as_dict()), 200)

    def put(self, post_id):
        post_put_args = reqparse.RequestParser()
        post_put_args.add_argument(
            "title", type=str, required=True, help="Post title is required"
        )
        post_put_args.add_argument("text", type=str, required=False)
        post_put_args.add_argument(
            "images", type=str, required=False, action="append"
        )
        post_put_args.add_argument("video_link", type=str, required=False)

        try:
            args = post_put_args.parse_args()
            try:
                post = PostModel.query.filter_by(id=post_id).first()
                if not post:
                    return make_response(jsonify({"error": f"Post with ID {post_id} not found"}), 404)
                for arg in args:
                    if arg in post.__table__.columns:
                        setattr(post, arg, args[arg])
                post.updated_at = datetime.datetime.now()
                db.session.add(post)
                db.session.commit()
                return make_response(jsonify(post.as_dict()), 200)
            except Exception as e:
                return make_response(jsonify({"error": f"An error occurred: {e._message}"}), 500)
        except BadRequest as e:
            return make_response(jsonify({"error": e.description}), e.code)

    def delete(self, post_id):
        if not PostModel.query.filter_by(id=post_id).first():
            return make_response(jsonify({"error": f"Post with ID {post_id} not found"}), 404)
        PostModel.query.filter_by(id=post_id).delete()
        db.session.commit()
        return make_response(jsonify({"message": f"Post with ID {post_id} deleted successfully"}), 200)

api.add_resource(Posts, '/api/posts')
api.add_resource(Post, '/api/posts/<int:post_id>')

@app.route('/', methods=['GET'])
def home():
    # return '<h1>Welcome to Blog!</h1>'
    posts = PostModel.query.all()
    posts_as_json = [post.as_dict() for post in posts]
    return render_template('home.html', posts=posts_as_json)

if __name__ == '__main__':
    app.run()