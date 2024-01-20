from flask import request

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from . import bp
from schema import UserSchema, UserSchemaNested
from models.user_model import UserModel

@bp.route('/user/<user_id>')
class User(MethodView):

    @bp.response(200, UserSchemaNested)
    def get(self, user_id):
        user = UserModel.query.get(user_id)
        if user:
            print(user.posts.all())
            return user
        else:
            abort(400, message="user not found")
    
    @jwt_required()
    @bp.arguments(UserSchema)      
    def put(self, user_data, user_id):
        user = UserModel.query.get(get_jwt_identity())
        if user and user.id == user_id:
            user.from_dict(user_data)
            user.commit()
            return {'message': f'{user.username} post update'}, 202
        abort(400, message = "invalid user")

    @jwt_required()    
    def delete(self, user_id):
        user = UserModel.query.get(get_jwt_identity())
        if user == user_id:
            user.delete()
            return {'message': f'User: {user.username} user deleted'}, 202
        return {'message': "invalid user"}, 400

@bp.route('/user')
class UserList(MethodView):

    @bp.response(200, UserSchema(many = True))
    def get(self):
        return UserModel.query.all()
    
    @bp.arguments(UserSchema)
    def post(self, user_data):
        try:
            user = UserModel()
            user.from_dict(user_data)
            user.commit()
            return { 'message' : f'{user_data["username"]} created' }, 201
        except:
            abort(400,message =  "Username and/or email taken")

@bp.route('/user/follow/<followed_id>')
class FollowUser(MethodView):
    
    @jwt_required()
    def post(self, followed_id):
        followed = UserModel.query.get(followed_id)
        follower =UserModel.query.get(get_jwt_identity())
        if follower and followed:
            follower.follow(followed)
            followed.commit()
            return {'message':'user followed'}
        else:
            return {'message':'invalid user'}, 400
        
    @jwt_required()  
    def put(self, followed_id):
        followed = UserModel.query.get(followed_id)
        follower = UserModel.query.get(get_jwt_identity())
        if follower and followed:
            follower.unfollow(followed)
            followed.commit()
            return {'message':'user unfollowed'}
        else:
            return {'message':'invalid user'}, 400


# user routes RETRIEVE
# @bp.response(200, UserSchema(many=True))
# @bp.get('/user')
# def user():
#     return { 'users': list(users.values())}, 200

#post routes CREATE

# @bp.route('/user', methods=["POST"])
# @bp.arguments(UserSchema)
# def create_user(user_data):
#     users[uuid4()] = user_data
#     return {'message' : f'{user_data["username"]} created'}, 201

# @bp.get('/user/<user_id>')
# @bp.response(200, UserSchema)
# def get_user(user_id):
#     try:
#         return {'user': users[user_id]}
#     except:
#         return {"message": 'invalid user'}, 400
    


    # abort({'message': "please include username, email and password"}, 400)
    

# UPDATE
# @bp.put('/user/<user_id>')
# def update_user(user_id):
#     try:
#         user = users[user_id]
#         user_data = request.get_json()
#         user |= user_data
#         return {'message': f'{user["username"]} post update'}, 202
#     except KeyError:
#         return{"message": "invalid user"}, 400
   

#DELETE
# @bp.delete('/user/<user_id>')
# def delete_user(user_id):
#     # user_data = request.get_json()
#     # username = user_data['username']
#     try:
#         del users[user_id]
#         return {'message': f' user deleted'}, 202
#     except:
#         return{"message": "invalid user"}, 400
