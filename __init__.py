import sys, os, shutil
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from .utilities_conversion import *
from .utilities_primitives import *
from .utilities_developer import *
from .utilities_images import *
from .utilities_conditioning import *
from .utilities_strings import *
from .utilities_passthroughs import *
from .common import *

NODE_CLASS_MAPPINGS = { 
                      # conditioning
                        "Two Clip Text Encode" : TwoClipTextEncode,
                      # conversion
                        "To String" : ConvertToString,
                        "To Int" : ConvertToInt,
                        "To Float" : ConvertToFloat,
                      # developer
                        "Inspect" : Inspect,
                      # images
                        "Image Size" : ImageSize,
                        "Resize Image" : ResizeImage,
                        "Combine Images" :CombineImages,
                      # primitives
                        "String_" : PrimitiveString,
                        "String Pair" : PrimitiveStringPair,
                        "Int_" : PrimitiveInt,
                        "Int Pair" : PrimitiveIntPair,
                        "Float_" : PrimitiveFloat,
                        "Float Pair" : PrimitiveFloatPair,
                      # strings
                        "Show Text" : ShowText,
                        "Regex Substitution" : RegexSub,                      
                      }

for m in PASSTHROUGH_MAPPINGS:
    NODE_CLASS_MAPPINGS[m] = PASSTHROUGH_MAPPINGS[m]

NODE_DISPLAY_NAME_MAPPINGS = {
                        "String_" : "String",
                        "Int_" : "Int",
                        "Float_" : "Float",   
}

for m in PASSTHROUGH_NAME_MAPPINGS:
    NODE_DISPLAY_NAME_MAPPINGS[m] = PASSTHROUGH_NAME_MAPPINGS[m]

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

shutil.copytree(module_js_directory_utilities, application_web_extensions_directory, dirs_exist_ok=True)
