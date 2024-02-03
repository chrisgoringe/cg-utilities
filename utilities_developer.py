from .base import BaseNode
   
class Inspect(BaseNode):
    CATEGORY = "utilities/developer"
    OPTIONAL = { "anything": ("*",{}) }
    OUTPUT_NODE = True

    def func(cls, anything=None):
        pass # put breakpoint here
        return()

class ComboPass(BaseNode):
    CATEGORY = "utilities/developer"
    REQUIRED = { "option": ([""],{})}
    RETURN_TYPES = ("*",)
    DESCRIPTION = "combo"
    OUTPUT_NODE = True
    def func(self, option):
        return {"ui":{"update":""}, "result":(option,)}
    @classmethod
    def VALIDATE_INPUTS(cls, **kwargs):
        return True
    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")