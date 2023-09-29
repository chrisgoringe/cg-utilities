import math, os, json
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import torch
import numpy as np

from comfy_extras.nodes_post_processing import Blur
from comfy.cli_args import args
import folder_paths

from custom_nodes.cg_custom_core.base import BaseNode
from custom_nodes.cg_custom_core.ui_decorator import ui_signal

@ui_signal('display_text')
class ImageSize(BaseNode):
    CATEGORY = "utilities/images"
    REQUIRED = { "image": ("IMAGE",), }
    RETURN_TYPES = ("INT","INT",)
    RETURN_NAMES = ("width","height",)

    def func(self, image:torch.Tensor):
        w, h = image.shape[2],image.shape[1]
        text = f"{w} x {h}"
        return (w,h,text)
    
class CombineImages(BaseNode):
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

@ui_signal('display_text') 
class ResizeImage(BaseNode):
    CATEGORY = "utilities/images"
    REQUIRED = { 
        "constraint": (["x8", "cn512", "none"],),
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

    def func(self, constraint:str, image:torch.tensor, factor:float=1.0, max_dimension:int=0, image_to_match:torch.tensor=None):
        if image_to_match is not None:
            height, width = image_to_match.shape[1:3]
        else:
            height, width = image.shape[1:3]

        if constraint!="cn512":
            height = height * factor
            width = width * factor

            too_big_by = max(height/max_dimension, width/max_dimension)
            if too_big_by > 1.0:
                height = math.floor(height/too_big_by)
                width = math.floor(width/too_big_by)

        if constraint=="x8":
            height = ((4+height)//8) * 8
            width = ((4+width)//8) * 8
        elif constraint=="cn512":
            if height >= width:
                height = (((height*512/width)+32)//64) * 64
                width = 512
            else:
                width = (((width*512/height)+32)//64) * 64
                height = 512

        height = int(height)
        width = int(width)
        
        return (self.resize(image, height, width),
                self.resize(image_to_match if image_to_match is not None else image, height, width),
                width, height, f"{width} x {height}") 

@ui_signal('display_text') 
class CompareImages(BaseNode):
    CATEGORY = "utilities/images"
    REQUIRED = { "image1": ("IMAGE",), "image2": ("IMAGE",), "multiplier": ("FLOAT", {"default":1.0})}
    RETURN_TYPES = ("IMAGE","IMAGE","FLOAT")
    RETURN_NAMES = ("all", "diff","mse",)
    lf = torch.nn.MSELoss()

    def func(self, image1:torch.Tensor, image2:torch.Tensor, multiplier:float):
        diff = torch.clamp(torch.abs(image1-image2) * multiplier, 0.0, 1.0)
        mean = torch.mean(diff,3)
        result = torch.stack([mean for _ in range(3)],3)
        combined = torch.cat((image1,image2,result),0)
        mean = torch.mean(diff.flatten())
        mse = float(self.lf(image1,image2))
        message = "MSE diff {:12.10f}".format(mse)
        return (combined, result, mse, message)
    
class MaskHardenAndBlur(BaseNode, Blur):
    CATEGORY = "utilities/images"
    REQUIRED = { "mask" : ("MASK", {}), 
                 "threshold" : ("FLOAT",{"default":0.5, "min":0.0, "max":1.0, "step":0.01}), 
                 "blur_radius": ("INT", {"default": 1, "min": 1, "max": 31, "step": 1 }),
                 "sigma": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 10.0, "step": 0.1 }),
                }
    RETURN_TYPES = ("MASK",)
    RETURN_NAMES = ("mask",)
    def func(self, mask, threshold, blur_radius, sigma):
        m = torch.where(mask>threshold,1.0,0.0)
        m = m.unsqueeze(2).unsqueeze(0)
        blurred:torch.Tensor = self.blur(m, blur_radius, sigma)[0].squeeze()
        return (blurred,)

class SaveImageAs(BaseNode):
    CATEGORY = "utilities/images"
    REQUIRED = {"image": ("IMAGE",), 
                "filename": ("STRING",{"default":""})}
    HIDDEN = {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"}
    OUTPUT_NODE = True
    def func(self, image, filename, prompt, extra_pnginfo):
        full_folder = os.path.join(folder_paths.get_output_directory(), os.path.dirname(os.path.normpath(filename)))
        if not os.path.exists(full_folder):
            os.makedirs(full_folder)
        filename = os.path.basename(os.path.normpath(filename))
        i = 255. * image[0].cpu().numpy()
        img = Image.fromarray(np.clip(i, 0, 255).astype(np.uint8))

        if not args.disable_metadata:
            metadata = PngInfo()
            if prompt is not None:
                metadata.add_text("prompt", json.dumps(prompt))
            if extra_pnginfo is not None:
                for x in extra_pnginfo:
                    metadata.add_text(x, json.dumps(extra_pnginfo[x]))

        img.save(os.path.join(full_folder, filename), pnginfo=metadata, compress_level=4)
        return ()