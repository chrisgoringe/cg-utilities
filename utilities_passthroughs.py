from .common import classproperty, module_root_directory_utilities
import json, os, sys
from nodes import NODE_CLASS_MAPPINGS

class PassthroughException(Exception):
    pass

class ReturnInput():
    CATEGORY = "utilities/passthrough"
    BASED_ON:type = None
    PASSED = []
    FUNCTION = "_func"

    def _func(self, **kwargs):
        s = getattr(self, getattr(self.BASED_ON,"FUNCTION"))(**kwargs) 
        return s + tuple(kwargs[r] for r in self.PASSED)
    
    @classmethod
    def INPUT_TYPES(cls):
        return cls.BASED_ON.INPUT_TYPES()
    
    @classproperty
    def RETURN_TYPES(cls):
        s = cls.BASED_ON.RETURN_TYPES 
        in_types = cls.INPUT_TYPES()
        for r in cls.PASSED:
            get_type = lambda key : in_types.get(key,{}).get(r,[None])[0]
            type = get_type('required') or get_type('optional') or get_type('hidden') or None
            if type is None:
                raise PassthroughException(f"input {r} not found in {cls.BASED_ON}")
            s = s + (r,)
        return s
    
    @classproperty
    def RETURN_NAMES(cls):
        s = cls.BASED_ON.RETURN_NAMES if hasattr(cls.BASED_ON, 'RETURN_NAMES') else cls.BASED_ON.RETURN_TYPES
        return s + tuple(cls.PASSED_RETURN_NAMES if hasattr(cls, 'PASSED_RETURN_NAMES') else cls.PASSED) 

def passthrough_factory(name, based_on_class, passed_input_list, category=None) -> type:
    return type(name, 
                (ReturnInput,based_on_class,), 
                {'BASED_ON':based_on_class, 'PASSED':passed_input_list, 'CATEGORY':category or ReturnInput.CATEGORY})

def create_passthroughs():
    MAP = {}
    DISPLAY_MAP = {}
    try:
        config_file = os.path.join(module_root_directory_utilities, "passthrough_config.json")
        with open(config_file, 'r') as file:
            items:dict = json.load(file)
            for i, key in enumerate(items):
                if key=='SHOW':
                    continue
                class_name = f"passthrough_class_{i}"
                based_on_clazz = NODE_CLASS_MAPPINGS[items[key]['based_on']]
                inputs_to_pass = items[key]['inputs_to_pass']
                category = items[key].get('category',None)
                clazz = passthrough_factory(class_name, based_on_clazz, inputs_to_pass, category)
            
            # If there seems to be a problem give a warning but add it anyway
            # in case the parent class has some weird dynamic RETURN_TYPEs
            # The core code will reject it if it wants to
                try:
                    clazz.RETURN_TYPES
                except PassthroughException:
                    print(f"In passthrough config, {key} failed validation: {sys.exc_info()[1].args[0]} ")

                MAP[class_name] = clazz
                DISPLAY_MAP[class_name] = items[key].get('display_name', key)
            
            if 'SHOW' in items and items['SHOW']:
                print("utilities_passthroughs: List of all unique names of node type that have been loaded and can be used in `based_on`:")
                for name in NODE_CLASS_MAPPINGS:
                    print(name)
            else:
                print("utilities_passthroughs: to see all nodes available set \"SHOW\" : 1 in passthrough_config.json")
                    
    except (KeyError,PassthroughException,json.decoder.JSONDecodeError):
        print(f"passthrough_config error - {sys.exc_info()[0]} - {sys.exc_info()[1]}")
    return MAP, DISPLAY_MAP

PASSTHROUGH_MAPPINGS, PASSTHROUGH_NAME_MAPPINGS = create_passthroughs()