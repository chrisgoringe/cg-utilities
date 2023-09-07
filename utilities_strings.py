from .common import Base_utilities, textdisplay
import re, datetime

@textdisplay
class ShowText(Base_utilities):
    CATEGORY = "utilities/strings"
    REQUIRED = { "text": ("STRING", {"forceInput": True}), }
    def func(self, text):
        return (text,)
    
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