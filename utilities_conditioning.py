from .common import Base_utilities
from nodes import CLIPTextEncode

class TwoClipTextEncode(Base_utilities):
    CATEGORY = "utilities/conditioning"
    REQUIRED = {"clip": ("CLIP", {}), "prompt": ("STRING", {"default":""}), "negative_prompt": ("STRING", {"default":""})}
    RETURN_TYPES = ("CONDITIONING", "CONDITIONING",)
    RETURN_NAMES = ("positive", "negative",)
    encoder = CLIPTextEncode().encode

    def func(self, clip, prompt, negative_prompt):
        return(self.encoder(clip,prompt)[0], self.encoder(clip,negative_prompt)[0], )