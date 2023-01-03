import graphene
from serializers import UserGrapheneInputModel, UserGrapheneModel, UserLoginGrapheneModel, UserLoginGrapheneInputModel,FbAccountGrapheneModel,FbEngagementsGrapheneInputModel,FbEngagementGrapheneModel
from models.user import User
from models.facebook_account import FacebookAccount
from models.fb_engagement import FbEngagement
from db import db
import bcrypt
from jose import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()



class Query(graphene.ObjectType):
    say_hello = graphene.String(name=graphene.String(default_value='Test Driven'))
    list_fb_account = graphene.List(FbAccountGrapheneModel)
    get_fbengagements = graphene.List(FbEngagementGrapheneModel, start_date=graphene.NonNull(graphene.DateTime),end_date=graphene.NonNull(graphene.DateTime))
    get_fbengagementsSummarize = graphene.List(FbEngagementGrapheneModel, account_id=graphene.NonNull(graphene.Int), start_date=graphene.NonNull(graphene.DateTime),end_date=graphene.NonNull(graphene.DateTime))
    

    @staticmethod
    def resolve_say_hello(parent, info, name):
        return f'Hello {name}'
    
    @staticmethod
    def resolve_list_fb_account(parent, info):
        return FacebookAccount.all().where('is_active', True)
    
 
    
    @staticmethod
    def resolve_get_fbengagements(parent, info, start_date, end_date):
        return  db.table('fb_engagements').where_between('updated_at', [start_date, end_date]).get().all()
    
    @staticmethod
    def resolve_get_fbengagementsSummarize(parent, info,account_id, start_date, end_date):
        summarize_data =db.table('fb_engagements').where_between('updated_at', [start_date, end_date]).where('account_id', account_id).get().sum('likes')
        summarize_data_shares =db.table('fb_engagements').where_between('updated_at', [start_date, end_date]).where('account_id', account_id).get().sum('shares')
        summarize_data_comments =db.table('fb_engagements').where_between('updated_at', [start_date, end_date]).where('account_id', account_id).get().count()
        summarize_data_list =db.table('fb_engagements').where_between('updated_at', [start_date, end_date]).where('account_id', account_id).get()
        acc_id = 0
        for i in summarize_data_list:
            acc_id=i.id
        
        summarize_data_list1 =db.table('fb_engagements').where('account_id', account_id).where('id',acc_id).get()
        for i in summarize_data_list1:
            i.likes = summarize_data
            i.shares = summarize_data_shares
            i.comments = summarize_data_comments
            acc_id=i.id
       
        return  summarize_data_list1

    
    

class CreateUser(graphene.Mutation):
    class Arguments:
        user_details = UserGrapheneInputModel()

    Output = UserGrapheneModel

    @staticmethod
    def mutate(parent, info, user_details):
        users = db.table('users').where('username', user_details.username).get()

        for user in users:
            if user['username'] == user_details.username:
                raise Exception('User with the given email already exists')
            
        user = User()
        user.username = user_details.username
        user.email = user_details.email
        user.access_token=""
        user.setPassword(user_details.password)
        user.save()

        return user
    
    
class LoginUser(graphene.Mutation):
    class Arguments:
        login_details = UserLoginGrapheneInputModel()

    Output = UserLoginGrapheneModel

    @staticmethod
    def mutate(parent, info, login_details):
            users = db.table('users').where('username', login_details.username).first()
            if users:
                
                userBytes = login_details.password.encode('utf-8')
                result = bcrypt.checkpw(userBytes, users['password'].encode('utf-8'))
                if users['username'] == login_details.username:
                    if result == True:
                        dt = datetime.now() + timedelta(minutes=2)           
                        encoded_token = jwt.encode({'user_id': str(users['id']), 'exp': dt }, os.getenv('SECRET_KEY'), algorithm='HS256')
                        users['access_token'] = encoded_token
                        last_loggedin = db.table('users').where('id', users['id']).update(updated_at=datetime.now())
                        create_access_token = db.table('users').where('id', users['id']).update(access_token=users['access_token'])
                        return users
                    else:
                        raise Exception('Invalid password')
                else:
                    raise Exception('Invalid username')
                
            else:
                raise Exception("User does not exits")
  
   
    
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()
