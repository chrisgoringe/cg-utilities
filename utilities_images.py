from .common import Base_utilities, classproperty
import torch
import math

class ImageSize(Base_utilities):
    CATEGORY = "utilities/images"
    REQUIRED = { "image": ("IMAGE",), }
    RETURN_TYPES = ("INT","INT")
    RETURN_NAMES = ("width","height")
    def func(self, image:torch.Tensor):
        return (image.shape[2],image.shape[1])
    
class CombineImages(Base_utilities):
    CATEGORY = "utilities/images"
    REQUIRED = { 
        "image1": ("IMAGE",) ,
    }
    OPTIONAL = {
        "image2": ("IMAGE",) ,
        "image3": ("IMAGE",) ,
        "image4": ("IMAGE",) ,
    }
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    def func(self, image1, image2=None, image3=None, image4=None):
        return (torch.cat( tuple(i for i in (image1, image2, image3, image4) if i is not None), 0 ),)
        
class ResizeImage(Base_utilities):
    CATEGORY = "utilities/images"
    REQUIRED = { 
        "x8": (["yes", "no"],),
        "image": ("IMAGE",),
        "factor": ("FLOAT", {"default":1.0, "min":0.0, "step":0.1 }),
        "max_dimension": ("INT", {"default": 10000, }), 
    }
    OPTIONAL = {
        "image_to_match": ("IMAGE",),
    }
    RETURN_TYPES = ("IMAGE","IMAGE","INT","INT",)
    RETURN_NAMES = ("image","matched_image","width","height",)

    @classmethod
    def resize(cls, image, height, width):
        h,w = image.shape[1:3]
        if h==height and w==width:
            return image
        permed = torch.permute(image,(0, 3, 1, 2))
        scaled = torch.nn.functional.interpolate(permed, size=(height, width))
        return torch.permute(scaled, (0, 2, 3, 1))

    def func(self, x8:str, image:torch.tensor, factor:float=1.0, max_dimension:int=0, image_to_match:torch.tensor=None):
        if image_to_match:
            height, width = image_to_match.shape[1:3]
        else:
            height, width = image.shape[1:3]

        height = height * factor
        width = width * factor

        too_big_by = max(height/max_dimension, width/max_dimension)
        if too_big_by > 1.0:
            height = math.floor(h*factor/too_big_by)
            width = math.floor(w*factor/too_big_by)

        if x8=="Yes":
            height = ((4+height)//8) * 8
            width = ((4+width)//8) * 8
        
        return (self.resize(image, height, width),
                self.resize(image_to_match or image, height, width),) 