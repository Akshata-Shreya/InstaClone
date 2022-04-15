from utils import post_handle
import uuid

id = uuid.uuid4()
userID = "b1f16884-2f48-4db2-bb2b-61825fb70c61"
# password = "shr123"

# user = {
#         "_id":str(id),
#         "username":name,
#         "password":password
#     }

# user_handle.insert_one(user)

post_handle.insert_one(
    {
        "_id":str(id),
        "userID":userID,
        "location":"Mumbai",
        "description":"Keep Smiling"
    }
)