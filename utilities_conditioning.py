from .common import Base_utilities
from nodes import CLIPTextEncode, ConditioningSetMask

class TwoClipTextEncode(Base_utilities):
    CATEGORY = "utilities/conditioning"
    REQUIRED = {"clip": ("CLIP", {}), "prompt": ("STRING", {"default":""}), "negative_prompt": ("STRING", {"default":""})}
    RETURN_TYPES = ("CONDITIONING", "CONDITIONING",)
    RETURN_NAMES = ("positive", "negative",)
    encoder = CLIPTextEncode().encode

    def func(self, clip, prompt, negative_prompt):
        return(self.encoder(clip,prompt)[0], self.encoder(clip,negative_prompt)[0], )
    
class MergeConditionings(Base_utilities):
    CATEGORY = "utilities/conditioning"
    REQUIRED = {"conditioning1": ("CONDITIONING", ), "conditioning2": ("CONDITIONING", ), "mask": ("MASK", ), }
    RETURN_TYPES = ("CONDITIONING", )
    RETURN_NAMES = ("conditioning", )
    apply_mask = ConditioningSetMask().append

    def func(self, conditioning1, conditioning2, mask):
        c1 = self.apply_mask(conditioning1, mask, "default", 1.0)[0]
        c2 = self.apply_mask(conditioning2, 1.0-mask, "default", 1.0)[0]
        return (c1+c2, )