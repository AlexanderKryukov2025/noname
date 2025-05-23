from .base_params import BaseParamsBuilder

class DevicesParamsBuilder(BaseParamsBuilder):
    def __init__(self):
        super().__init__()
        self.params.update({
            "page": 1,
            "filter[client_id]": None,
            "filter[org_struct_lvl1_id]": None,
            "filter[org_struct_lvl2_id]": None,
            "filter[serial_number]": None,
            "filter[side_number]": None,
            "filter[device_name]": None,
            "filter[device_type]": None,
            "filter[status]": None,
            "filter[version]": None,
            "filter[online]": None,
            "filter[offline]": None,
            "filter[defective]": None,
            "filter[working]": None
        })

# Пример использования:
# builder = DevicesParamsBuilder()
# params = builder.set_param("filter[device_type]", "sensor").set_param("filter[status]", "active").build()
# print(params)

# Можно также добавлять методы для удобства, например:
class DevicesParams(DevicesParamsBuilder):
    def __init__(self):
        super().__init__()

    def set_page_num(self, page_num):
        return self.set_param("page", page_num)

    def set_client_id(self, client_id):
        return self.set_param("filter[client_id]", client_id)

    def set_org_struct_lvl1_id(self, id):
        return self.set_param("filter[org_struct_lvl1_id]", id)

    def set_org_struct_lvl2_id(self, id):
        return self.set_param("filter[org_struct_lvl2_id]", id)

    def set_serial_number(self, serial_number):
        return self.set_param("filter[serial_number]", serial_number)

    def set_side_number(self, side_number):
        return self.set_param("filter[side_number]", side_number)

    def set_device_name(self, name):
        return self.set_param("filter[device_name]", name)

    def set_device_type(self, device_type):
        return self.set_param("filter[device_type]", device_type)

    def set_status(self, status):
        return self.set_param("filter[status]", status)

    def set_version(self, version):
        return self.set_param("filter[version]", version)

    def set_online(self, is_online=True):
        return self.set_param("filter[online]", is_online)

    def set_offline(self, is_offline=True):
        return self.set_param("filter[offline]", is_offline)

    def set_defective(self, is_defective=True):
        return self.set_param("filter[defective]", is_defective)

    def set_working(self, is_working=True):
        return self.set_param("filter[working]", is_working)

# Пример использования:
# device_filters = DevicesParams()
# device_filters.set_client_id(123).set_status("active").set_device_type("sensor")
# print(device_filters.build()