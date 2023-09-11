import os
import folder_paths

module_root_directory_utilities = os.path.dirname(os.path.realpath(__file__))
module_js_directory_utilities = os.path.join(module_root_directory_utilities, "js")

application_root_directory = os.path.dirname(folder_paths.__file__)
application_web_extensions_directory = os.path.join(application_root_directory, "web", "extensions", "cg-nodes", "utilities")

class Base_utilities:
    def __init__(self):
        pass
    FUNCTION = "func"
    CATEGORY = "utilities"
    REQUIRED = {}
    OPTIONAL = None
    HIDDEN = None
    @classmethod    
    def INPUT_TYPES(s):
        types = {"required": s.REQUIRED}
        if s.OPTIONAL:
            types["optional"] = s.OPTIONAL
        if s.HIDDEN:
            types["hidden"] = s.HIDDEN
        return types
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    
class classproperty(object):
    def __init__(self, f):
        self.f = f
    def __get__(self, obj, owner):
        return self.f(owner)
    
