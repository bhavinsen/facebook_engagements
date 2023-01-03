from typing import List, Optional

from graphene_pydantic import PydanticInputObjectType, PydanticObjectType
from pydantic import BaseModel
from datetime import date, datetime



class UserModel(BaseModel):
    id: int
    username: str
    email: str
    password: str
    access_token: str
    
class FbAccountModel(BaseModel):
    id: int
    account_id: int
    account_name: str
    is_active: bool
    
class FbEngagementModel(BaseModel):
    id: int
    account_id: int
    likes: int
    shares: int
    comments: str
    from_date: datetime
    to_date: datetime
    account_name:str
    
# class UserFBModel(BaseModel):
#     username: str
    
    
    
    
class UserGrapheneModel(PydanticObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ('access_token',)
        

class UserGrapheneInputModel(PydanticInputObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ('id', 'access_token')
        
class UserLoginGrapheneModel(PydanticObjectType):
    class Meta:
        model = UserModel
        
        

class UserLoginGrapheneInputModel(PydanticInputObjectType):
    class Meta:
        model = UserModel
        exclude_fields = ('id', 'email', 'access_token')
        
        
# class UserGrapheneFBInputModel(PydanticObjectType):
#     class Meta:
#         model = UserFBModel
        
        

# class UserGrapheneFBModel(PydanticInputObjectType):
#     class Meta:
#         model = UserFBModel
#         exclude_fields = ('id',)
        
class FbAccountGrapheneModel(PydanticObjectType):
    class Meta:
        model = FbAccountModel
        exclude_fields = ('id',)
        
class FbEngagementsGrapheneInputModel(PydanticInputObjectType):
    class Meta:
        model = FbEngagementModel
        exclude_fields = ('id', 'account_id', 'likes', 'shares', 'comments')
        
class FbEngagementGrapheneModel(PydanticObjectType):
    class Meta:
        model = FbEngagementModel