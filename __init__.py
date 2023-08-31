import sys, os
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)))
from .utilities_conversion import *
from .utilities_primitives import *
from .utilities_developer import *
from .utilities_images import *
from .utilities_conditioning import *

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
                      }

NODE_DISPLAY_NAME_MAPPINGS = {
                        "String_" : "String",
                        "Int_" : "Int",
                        "Float_" : "Float",   
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
