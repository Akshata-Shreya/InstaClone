from utils import user_handle
import uuid

id = uuid.uuid4()
username = "shreshtha"
password = "shresh"
bio = "Sleepy shreya ki dost"
name = "Shreshtha Sharma"
followers = []
following = []
# user = {
#         "_id":str(id),
#         "username":name,
#         "password":password
#     }

# user_handle.insert_one(user)

user_handle.insert_one(
    {
        "_id":str(id),
        "username":username,
        "password":password,
        "bio":bio,
        "name":name,
        "userID":str(id),
        "followers": followers,
        "following":following
    }
)