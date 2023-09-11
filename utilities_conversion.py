from custom_nodes.cg_custom_core.base import BaseNode, classproperty
   
class ConvertToString(BaseNode):
    CATEGORY = "utilities/conversion"
    OPTIONAL = { "anything": ("*",{}) }

    TYPE = "STRING"
    DEFAULT = ""
    CONVERT = lambda a : str(a)

    @classproperty
    def RETURN_TYPES(cls):
        return (cls.TYPE,)
    
    @classproperty
    def RETURN_NAMES(cls):
        return (cls.TYPE.lower(),)
    
    @classmethod
    def func(cls, anything=None):
        try:
            return (cls.CONVERT(anything),)
        except:
            return (cls.DEFAULT,)
        
class ConvertToInt(ConvertToString):
    TYPE = "INT"
    DEFAULT = 0
    CONVERT = lambda a : int(a)

class ConvertToFloat(ConvertToString):
    TYPE = "FLOAT"
    DEFAULT = 0
    CONVERT = lambda a : float(a)
