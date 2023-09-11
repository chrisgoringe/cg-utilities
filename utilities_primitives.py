from custom_nodes.cg_custom_core.base import BaseNode, classproperty
   
class PrimitiveString(BaseNode):
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
