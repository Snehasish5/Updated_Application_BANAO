# models.py (MongoDB version)

from flask_login import UserMixin

# User model as a Python class
class User(UserMixin):
    def __init__(self, data):
        self.id = str(data.get('_id'))  # MongoDB uses ObjectId
        self.username = data.get('username')
        self.password = data.get('password')
        self.role = data.get('role')
        self.email = data.get('email')
        self.first_name = data.get('first_name')
        self.last_name = data.get('last_name')
        self.profile_pic = data.get('profile_pic')
        self.address_line = data.get('address_line')
        self.city = data.get('city')
        self.state = data.get('state')
        self.pincode = data.get('pincode')

    def get_id(self):
        return self.id


# Blog model is handled as a dictionary document
# You can manipulate blogs directly in views like:
# mongo.db.blogs.insert_one(blog_dict)
# or mongo.db.blogs.find({'author_id': user_id})
