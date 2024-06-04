from entities.models import *


class LoginModel(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_user_by_user_name(self, user_name):
        query: User = User.get(User.user_name == user_name)
        return query

    def is_exist(self, user_name):
        query = User.select().where(User.user_name == user_name).exists()
        return query

    def change_password(self, user_id, new_password):
        query = User.update(password=new_password).where(User.id == user_id)
        result = query.execute()
        return result

