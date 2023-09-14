from custom_nodes.cg_custom_core.base import BaseNode
from custom_nodes.cg_custom_core.ui_decorator import ui_signal
import re, datetime

@ui_signal('display_text')
class ShowText(BaseNode):
    CATEGORY = "utilities/strings"
    REQUIRED = { "text": ("STRING", {"forceInput": True}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    def func(self, text):
        return (text,text,)
    
class RegexSub(BaseNode):
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
        
class Substitute(BaseNode):
    CATEGORY = "utilities/strings"
    REQUIRED = {"template": ("STRING", {"default":"", "multiline": True })}
    OPTIONAL = { "x": ("*", {}), "y": ("*", {}) }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("string",)
    def func(self, template:str, x="", y=""):
        return (template.replace("[X]",str(x)).replace("[Y]",str(y)).replace(r"%date%",self.date_str()),)
    def date_str(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')    