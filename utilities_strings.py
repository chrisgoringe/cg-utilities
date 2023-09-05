from .common import Base_utilities
import re

class ShowText(Base_utilities):
    CATEGORY = "utilities/strings"
    REQUIRED = { "text": ("STRING", {"forceInput": True}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text_displayed",)
    OUTPUT_NODE = True

    def func(self, text):
        return {"ui": {"text_displayed": text}, "result": (text,)}
    
class RegexSub(Base_utilities):
    CATEGORY = "utilities/strings"
    REQUIRED = {"text": ("STRING", {"forceInput": True}), 
                "pattern": ("STRING", {"default": "" }),
                "replacement": ("STRING", {"default": ""}),
                }
    RETURN_TYPES = ("STRING","INT",)
    RETURN_NAMES = ("text","n_subs",)

    def func(self, text, pattern, replacement):
        try:
            return re.subn(pattern, replacement, text)
        except:
            print("Exception in RegexSub")
            return (text,0,)
        