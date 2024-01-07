from flask import request
from uuid import uuid4

from app import app
from db import posts, users
#POST

@app.post('/post')
def create_post():
    post_data = request.get_json()
    user_id = post_data['user_id']
    if user_id in users:
        posts[uuid4()] = post_data
        return {'message': "post created"}, 201
    return {'message': "invalid user"}, 401


@app.get('/post')
def get_posts():
    return {'post': list(posts.values())}

@app.get('/post/<post_id>')
def get_post(post_id):
    try:
        return {'post': posts[post_id]},200
    except KeyError:
        return {"message": 'invalid post'}, 400

@app.put('/post/<post_id>')
def update_post(post_id):
    try:
        post = posts[post_id]
        post_data = request.get_json()
        if post_data['user_id'] == post['user_id']:
            post['body'] = post_data['body']
            return {'message': 'post update'}, 202
        return{"message": "Unautho"}, 401
    except:
        return{"message": "invalid post id"}, 400

@app.delete('/post/<post_id>')
def delete_post(post_id):
    try:
        del posts[post_id]
        return {'message': ' post deleted'}, 202
    except:
        return{"message": "invalid user"}, 400
    