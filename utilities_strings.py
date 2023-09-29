from custom_nodes.cg_custom_core.base import BaseNode
from custom_nodes.cg_custom_core.ui_decorator import ui_signal
import re, datetime, json

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

class JSONDictionaryKey(BaseNode):
    CATEGORY = "utilities/strings"
    REQUIRED = {"text": ("STRING", {"forceInput": True}), 
                "key": ("STRING", {"default": "" }),
                } 
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("value",)
    def func(self, text, key):
        try:
            d = json.loads(text)[key]
            if isinstance(d,str):
                return (d.encode('utf-8','ignore').decode("utf-8"),)
            return (json.dumps(d),) 
        except:
            print("Exception in RegexSub")
            return ("",)
        
class RegexExtract(BaseNode):
    CATEGORY = "utilities/strings"
    REQUIRED = {"text": ("STRING", {"forceInput": True}), 
                "pattern": ("STRING", {"default": "" }),
                }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("match",)

    def func(self, text, pattern):
        try:
            z = re.search(pattern, text)
            return (z.group(0),) if z else ("",)
        except:
            print("Exception in RegexSub")
            return ("",)
        
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

class SimpleLog(BaseNode):
    CATEGORY = "utilities/strings"
    REQUIRED = {"log": ("STRING", {"forceInput" : True })}
    OUTPUT_NODE = True
    def func(self, log):
        print(log)
        return ()