from flask import Flask, request
from uuid import uuid4
app = Flask(__name__)

#CRUD
# c = create
# r=retreive
# u=upodate
# d=delete

users = {
    '1' : {
        'username':'dsmith',
        'email':'dsmit@cd.com'
    },
    '2' : {
        'username':'brandt',
        'email':'brandt@cd.com'
    }
}

posts = {
    '1':{
        'body' : 'FLASK WEEK LET GO!!!!',
        'user_id': '1'
    },
    '2':{
        'body' : 'whiteboard was killer',
        'user_id': '2'
    },
    '3':{
        'body' : 'servers',
        'user_id': '3'
    }
}
#user routes RETRIEVE
@app.get('/user')
def user():
    return { 'users': list(users.values())}

#post routes CREATE

@app.post('/user')
def create_user():
    json_body = request.get_json()
    users[uuid4()] = json_body
    return {'message' : f'{json_body["username"]} created'}, 201

# UPDATE
@app.put('/user')
def update_user():
    return

#DELETE
@app.delete('/user')
def delete_user():
    pass

@app.post('/post')
def create_post():
    pass

@app.get('/post')
def get_post():
    return {'post': list(posts.values())}

@app.put('/post')
def update_post():
    return

@app.delete('/post')
def delete_post():
    pass
    