from .common import Base_utilities, classproperty
   
class PrimitiveString(Base_utilities):
    CATEGORY = "utilities/primitives"
    TYPE = "STRING"
    DEFAULT = ""

    @classproperty
    def REQUIRED(cls):
        return { "value": (cls.TYPE, {"default": cls.DEFAULT}) }

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

class PrimitiveFloat(PrimitiveString):
    TYPE = "FLOAT"
    DEFAULT = 0.0

class PrimitiveStringPair(Base_utilities):
    CATEGORY = "utilities/primitives"
    TYPE = "STRING"
    DEFAULT = ""

    @classproperty
    def REQUIRED(cls):
        return { "value1": (cls.TYPE, {"default": cls.DEFAULT}), "value2": (cls.TYPE, {"default": cls.DEFAULT})  }

    @classproperty
    def RETURN_TYPES(cls):
        return (cls.TYPE,cls.TYPE,)
    
    @classproperty
    def RETURN_NAMES(cls):
        return (cls.TYPE.lower()+"1",cls.TYPE.lower()+"2",)
    
    @classmethod
    def func(cls, value1, value2,):
        return (value1,value2,)
    
class PrimitiveIntPair(PrimitiveStringPair):
    TYPE = "INT"
    DEFAULT = 0

class PrimitiveFloatPair(PrimitiveStringPair):
    TYPE = "FLOAT"
    DEFAULT = 0.0