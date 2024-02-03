from .base import BaseNode
import re, datetime, json
    
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
            js = json.loads(text)
            for k in key.split(','):
                js = js[k]
            if isinstance(js,str):
                return (js.encode('utf-8','ignore').decode("utf-8"),)
            return (json.dumps(js, indent=2),) 
        except:
            print("Exception in JSONDictionaryKey")
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
        return (template.replace("[X]",str(x)).replace("[Y]",str(y)).replace(r"%date%",self.date_str()).replace('\ufeff',''),)
    def date_str(self):
        return datetime.datetime.today().strftime('%Y-%m-%d')    