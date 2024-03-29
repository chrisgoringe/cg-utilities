from .base import BaseNode, classproperty
   
class PrimitiveString(BaseNode):
    CATEGORY = "utilities/primitives"
    TYPE = "STRING"
    DEFAULT = ""

    @classproperty
    def REQUIRED(cls):
        return { "value": (cls.TYPE, {"default": cls.DEFAULT, "multiline": True, "label":"LABEL!"}) }

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
    
class PrimitiveSeed(PrimitiveInt):
    @classproperty
    def REQUIRED(cls):
        return { "seed": (cls.TYPE, {"default": cls.DEFAULT, "min":0, "max": 0xffffffffffffffff}) }
    @classmethod
    def func(cls, seed):
        return (seed,)

class PrimitiveFloat(PrimitiveInt):
    TYPE = "FLOAT"
    DEFAULT = 0.0
