class EmployeeController:
    def __init__(self):
        pass

    def save(self, model):
        print("Save employee")

    def update(self, id, model):
        print(id)
        print(model)

    def delete(self, id):
        print(id)

    def search(self, request_model):
        print(request_model)