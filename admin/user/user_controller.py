class UserController:
    def __init__(self):
        pass

    def login(self, username, password):
        if username == 'admin' and password == 'Abc@123':
            # Get data from db and then compare before allow login into system
            print("login successful")
        else:
            print("login failed")

