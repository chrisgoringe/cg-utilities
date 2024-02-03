import sys, os, shutil, git
import folder_paths

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from .utilities_conversion import *
from .utilities_primitives import *
from .utilities_developer import *
from .utilities_images import *
from .utilities_conditioning import *
from .utilities_strings import *
from .utilities_passthroughs import *

module_root_directory = os.path.dirname(os.path.realpath(__file__))
module_js_directory = os.path.join(module_root_directory, "js")

NODE_CLASS_MAPPINGS = { 
                      # conditioning
                        "Two Clip Text Encode" : TwoClipTextEncode,
                        "Merge Conditionings" : MergeConditionings,
                      # conversion
                        "To String" : ConvertToString,
                        "To Int" : ConvertToInt,
                        "To Float" : ConvertToFloat,
                      # developer
                        "Inspect" : Inspect,
                        "ComboPass" : ComboPass,
                      # images
                        "Image Size" : ImageSize,
                        "Resize Image" : ResizeImage,
                        "Combine Images" : CombineImages,
                        "Compare Images" : CompareImages,
                        "Mask Harden and Blur" : MaskHardenAndBlur,
                        "Save Image As" : SaveImageAs,
                      # primitives
                        "String_" : PrimitiveString,
                        "Int_" : PrimitiveInt,
                        "Seed_" : PrimitiveSeed,
                        "Float_" : PrimitiveFloat,
                      # strings
                        "Regex Substitution" : RegexSub,      
                        "Regex Extraction" : RegexExtract,    
                        "Substitute" : Substitute,      
                        "JSON Dictionary Key" : JSONDictionaryKey,
                      # info
                        "Passthrough Info" : PassthroughInfo,    
                      }

for m in PASSTHROUGH_MAPPINGS:
    NODE_CLASS_MAPPINGS[m] = PASSTHROUGH_MAPPINGS[m]

NODE_DISPLAY_NAME_MAPPINGS = {
                        "String_" : "String",
                        "Int_" : "Int",
                        "Float_" : "Float",   
                        "Seed_" : "Seed",   
}

for m in PASSTHROUGH_NAME_MAPPINGS:
    NODE_DISPLAY_NAME_MAPPINGS[m] = PASSTHROUGH_NAME_MAPPINGS[m]

WEB_DIRECTORY = "./js"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']

