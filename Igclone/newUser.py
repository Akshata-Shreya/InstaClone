from utils import user_handle
import uuid

id = uuid.uuid4()
name = "shreya"
password = "shr123"

# user = {
#         "_id":str(id),
#         "username":name,
#         "password":password
#     }

# user_handle.insert_one(user)

user_handle.insert_one(
    {
        "_id":str(id),
        "username":name,
        "password":password
    }
)