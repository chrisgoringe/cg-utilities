from .common import Base_utilities
from custom_nodes.cg_custom_core.ui_decorator import ui_signal
import re, datetime
from comfy_extras.ui_decorator import ui_signal

@ui_signal('display_text')
class ShowText(Base_utilities):
    CATEGORY = "utilities/strings"
    REQUIRED = { "text": ("STRING", {"forceInput": True}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    def func(self, text):
        return (text,text,)
    
class RegexSub(Base_utilities):
    CATEGORY = "utilities/strings"
    REQUIRED = {"text": ("STRING", {"forceInput": True}), 
                "pattern": ("STRING", {"default": "" }),
                "replacement": ("STRING", {"default": ""}),
                }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    def func(self, text, pattern, replacement):
        try:
            return (re.sub(pattern, replacement, text),)
        except:
            print("Exception in RegexSub")
            return (text,)
        
class Substitute(Base_utilities):
    CATEGORY = "utilities/strings"
    REQUIRED = {"template": ("STRING", {"default":"", "multiline": True })}
    OPTIONAL = { "x": ("*", {}), "y": ("*", {}), "z": ("*", {}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, template:str, x="", y="", z=""):
        return (template.replace("[X]",str(x)).replace("[Y]",str(y)).replace("[Z]",str(z)).replace(r"%date%",self.date_str()),)
    def date_str(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')    