from payslip.pay_slip_model import PaySlipModel

class PaySlipController:
    def __init__(self):
        self.__pay_slip_model = PaySlipModel()

    def add_new(self, **new_data):
        try:
            save_result = self.__pay_slip_model.save(**new_data)
            return save_result
        except Exception as ex:
            print(ex)

    def delete_by_id(self, id):
        try:
            result = self.__pay_slip_model.delete(id)
            return result
        except Exception as ex:
            print(ex)

    def get_all(self, **search_conditions):
        try:
            data = self.__pay_slip_model.get_all(**search_conditions)
            return data
        except Exception as ex:
            print(ex)

    def update_by_id(self, id, new_data):
        try:
            save_result = self.__pay_slip_model.update(id, new_data)
            if save_result > 0:
                return 1
            else:
                return 0
        except Exception as e:
            print("[!Exc:", e)
            return 0

    def get_pay_slip_by_user_id(self, user_id):
        try:
            data = self.__pay_slip_model.get_pay_slip_by_userid({'user_id': user_id})
            return data
        except Exception as e:
            print("[!Exc:", e)
            return 0


