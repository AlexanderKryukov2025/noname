class BaseParamsBuilder:
    def __init__(self):
        self.params = {}

    def set_param(self, key, value):
        if isinstance(value, list):
            for idx, item in enumerate(value):
                param_key = f"{key}[{idx}]"
                self.params[param_key] = item
        else:
            if key in self.params:
                self.params[key] = value
        return self

    def set_params(self, params_dict):
        for key, value in params_dict.items():
            self.set_param(key, value)
        return self

    def build(self):
        return {k: v for k, v in self.params.items() if v is not None}
