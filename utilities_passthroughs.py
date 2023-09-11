from custom_nodes.cg_custom_core.base import BaseNode, classproperty
from custom_nodes.cg_custom_core.ui_decorator import ui_signal
import json, os, sys
from nodes import NODE_CLASS_MAPPINGS
module_root_directory = os.path.dirname(os.path.realpath(__file__))

class PassthroughException(Exception):
    pass

class ReturnInput():
    CATEGORY = "utilities/passthrough"
    BASED_ON:type = None
    PASSED = PASSED_RETURN_NAMES = PASSED_TYPES = []
    FUNCTION = "_func"

    def cloner(self, item, in_type):
        if in_type=="LATENT":
            r = {}
            for key in item:
                r[key] = item[key].clone()
        elif in_type=="IMAGE":
            r = item.clone()
        else:
            r = item
        return r
    
    def _func(self, **kwargs):
        additional = tuple(self.cloner(kwargs[r], self.PASSED_TYPES[i]) for i, r in enumerate(self.PASSED))
        s = getattr(self, getattr(self.BASED_ON,"FUNCTION"))(**kwargs) 
        return s + additional
    
    @classmethod
    def INPUT_TYPES(cls):
        return cls.BASED_ON.INPUT_TYPES()
    
    @classproperty
    def RETURN_TYPES(cls):
        s = cls.BASED_ON.RETURN_TYPES 
        in_types = cls.INPUT_TYPES()
        cls.PASSED_TYPES = []
        for r in cls.PASSED:
            get_type = lambda key : in_types.get(key,{}).get(r,[None])[0]
            type = get_type('required') or get_type('optional') or get_type('hidden') or None
            if type is None:
                raise PassthroughException(f"input {r} not found in {cls.BASED_ON}")
            cls.PASSED_TYPES.append(type)
        return s + tuple(cls.PASSED_TYPES)
    
    @classproperty
    def RETURN_NAMES(cls):
        s = cls.BASED_ON.RETURN_NAMES if hasattr(cls.BASED_ON, 'RETURN_NAMES') else cls.BASED_ON.RETURN_TYPES
        if hasattr(cls, 'PASSED_RETURN_NAMES') and cls.PASSED_RETURN_NAMES:
            return s + tuple(cls.PASSED_RETURN_NAMES) 
        else:
            return s + tuple(cls.PASSED)

def passthrough_factory(name, based_on_class, passed_input_list, passed_return_names, clone, category) -> type:
    return type(name, 
                (ReturnInput,based_on_class,), 
                {'BASED_ON':based_on_class, 
                 'PASSED':passed_input_list, 
                 'PASSED_RETURN_NAMES':passed_return_names,
                 'CLONE':clone,
                 'CATEGORY':category or ReturnInput.CATEGORY})

@ui_signal('display_text')
class PassthroughInfo(BaseNode):
    CATEGORY = "utilities/info"
    RETURN_TYPES = ()
    RETURN_NAMES = ()
    NAMES = CREATED = FAILED = []
    def func(self):
        s = ("\n".join(["Errors:",]+self.FAILED)+"\n\n" if self.FAILED else "") +\
               ("\n".join(["Classes created:",]+self.CREATED)+"\n\n" if self.CREATED else "") +\
               ("\n".join(["Classes available:",]+self.NAMES)+"\n\n" if self.NAMES else "")
        return (s,)

def create_passthroughs():
    MAP = {}
    DISPLAY_MAP = {}
    PassthroughInfo.NAMES = [n for n in NODE_CLASS_MAPPINGS]
    PassthroughInfo.CREATED = []
    PassthroughInfo.FAILED = []

    try:
        config_file = os.path.join(module_root_directory, "passthrough_config.json")
        with open(config_file, 'r') as file:
            items:dict = json.load(file)
            for key in items:
                try:
                    based_on_clazz = NODE_CLASS_MAPPINGS[items[key]['based_on']]
                    inputs_to_pass = items[key]['inputs_to_pass']
                    passed_return_names = items[key].get('passed_return_names',None)
                    category = items[key].get('category',None)
                    clone = items[key].get('clone', None)
                    clazz = passthrough_factory(key, based_on_clazz, inputs_to_pass, passed_return_names, clone, category)
                    print (f"Added node {key} as passthrough")
                
                # If there seems to be a problem give a warning but add it anyway
                # in case the parent class has some weird dynamic RETURN_TYPEs
                # The core code will reject it if it wants to
                    try:
                        clazz.RETURN_TYPES
                    except PassthroughException:
                        print(f"In passthrough config, {key} failed validation: {sys.exc_info()[1].args[0]} ")

                    MAP[key] = clazz
                    DISPLAY_MAP[key] = items[key].get('display_name', key)
                    PassthroughInfo.CREATED.append(DISPLAY_MAP[key])
                except:
                    print(f"In passthrough config, {key} failed") 
                    PassthroughInfo.FAILED.append(key)
                        
    except (KeyError,PassthroughException,json.decoder.JSONDecodeError):
        print(f"passthrough_config error - {sys.exc_info()[0]} - {sys.exc_info()[1]}")
    return MAP, DISPLAY_MAP

PASSTHROUGH_MAPPINGS, PASSTHROUGH_NAME_MAPPINGS = create_passthroughs()