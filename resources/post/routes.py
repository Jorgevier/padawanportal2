from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from uuid import uuid4
from flask.views import MethodView
from flask_smorest import abort

from models import PostModel

from schema import PostSchema, PostSchemaNested

from . import bp

#POST

@bp.route('/<post_id>')
class Post(MethodView):

    @bp.response(200, PostSchemaNested)
    def get(self, post_id):
        post = PostModel.query.get(post_id)
        if post:
            return post 
        abort(400, message='Invalid POst')


    @bp.arguments(PostSchema)
    def put(self, post_data ,post_id):
        post = PostModel.query.get(post_id)
        if post:
            post.body = post_data['body']
            post.commit()
            return {"message": "post updated"}, 201
        return {'message': "Invalid Post Id"}, 400

    def delete(self, post_id):
        post = PostModel.query.get(post_id)
        if post:
            post.delete()
            return {"message": "Post Deleted"}, 202
        return {'message':"Invalid Post"}, 400

@bp.route('/')
class PostList(MethodView):

    @bp.response(200, PostSchema(many = True))    
    def get(self):
        return PostModel.query.all()
    
    @jwt_required()
    @bp.arguments(PostSchema)
    def post(self, post_data):
        try:
            post = PostModel()
            post.user_id = get_jwt_identity()
            post.body = post_data['body']
            post.commit()
            return { 'message': "Post Created" }, 201
        except:
            return { 'message': "Invalid User"}, 401
       
    
# @bp.post('/')
# def create_post():
#     post_data = request.get_json()
#     user_id = post_data['user_id']
#     if user_id in users:
#         posts[uuid4()] = post_data
#         return {'message': "post created"}, 201
#     return {'message': "invalid user"}, 401


# @bp.get('/')
# def get_posts():
#     return {'posts': list(posts.values())}

# @bp.get('/<post_id>')
# def get_post(post_id):
#     try:
#         return {'post': posts[post_id]},200
#     except KeyError:
#         return {"message": 'invalid post'}, 400

# @bp.put('/<post_id>')
# def update_post(post_id):
#     try:
#         post = posts[post_id]
#         post_data = request.get_json()
#         if post_data['user_id'] == post['user_id']:
#             post['body'] = post_data['body']
#             return {'message': 'post update'}, 202
#         return{"message": "Unautho"}, 401
#     except:
#         return{"message": "invalid post id"}, 400

# @bp.delete('/<post_id>')
# def delete_post(post_id):
#     try:
#         del posts[post_id]
#         return {'message': ' post deleted'}, 202
#     except:
#         return{"message": "invalid user"}, 400
    