from pay_grade.pay_grade_model import PayGradeModel


class PayGradeController:
    def __init__(self):
        self.__pay_grade_model = PayGradeModel()

    def add_new(self, **new_data):
        try:
            result = self.__pay_grade_model.save(**new_data)
            return result
        except Exception as ex:
            print(ex)

    def delete_by_id(self, id):
        try:
            result = self.__pay_grade_model.delete(id)
            return result
        except Exception as ex:
            print(ex)

    def get_all(self, **conditions):
        try:
            data = self.__pay_grade_model.search(**conditions)
            return data
        except Exception as ex:
            print(ex)

    def update_by_id(self, id, new_data):
        try:
            save_result = self.__pay_grade_model.update(id, new_data)
            if save_result > 0:
                return 1
            else:
                return 0
        except Exception as e:
            print(e)
            return 0
