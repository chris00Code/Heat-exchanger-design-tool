import json

def validate_positive_integer(func):
    def wrapper(value):
        if not (isinstance(value, float) and value > 0):
            raise ValueError("The value must be a positive float.")
        func(value)

    return wrapper


class Flow:
    def __init__(self, fluid, temperature, mass_flow_rate):
        self.fluid = self.val_fluid(fluid)
        #@TODO valdate func return val
        self.temperature = self.val_temp(temperature)
        self.mass_flow_rate = self.val_mfr(mass_flow_rate)

    @staticmethod
    def val_fluid(fluid):
        if fluid in ["water", "air"]:
            return fluid
        else:
            raise NotImplementedError

    @staticmethod
    @validate_positive_integer
    def val_temp(temp):
        return temp

    @staticmethod
    @validate_positive_integer
    def val_mfr(mfr):
        return mfr

    def serialize(self):
        return None
        #return self.__dict__

