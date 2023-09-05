from .common import Base_utilities, classproperty
   
class PrimitiveString(Base_utilities):
    CATEGORY = "utilities/primitives"
    TYPE = "STRING"
    DEFAULT = ""

    @classproperty
    def REQUIRED(cls):
        return { "value": (cls.TYPE, {"default": cls.DEFAULT, "multiline": True}) }

    @classproperty
    def RETURN_TYPES(cls):
        return (cls.TYPE,)
    
    @classproperty
    def RETURN_NAMES(cls):
        return (cls.TYPE.lower(),)
    
    @classmethod
    def func(cls, value):
        return (value,)
        
class PrimitiveInt(PrimitiveString):
    TYPE = "INT"
    DEFAULT = 0
    @classproperty
    def REQUIRED(cls):
        return { "value": (cls.TYPE, {"default": cls.DEFAULT}) }

class PrimitiveFloat(PrimitiveInt):
    TYPE = "FLOAT"
    DEFAULT = 0.0
