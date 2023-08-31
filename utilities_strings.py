from .common import Base_utilities

class ShowText(Base_utilities):
    CATEGORY = "utilities/strings"
    REQUIRED = { "text": ("STRING", {"forceInput": True}), }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    OUTPUT_NODE = True

    def func(self, text):
        return {"ui": {"text": text}, "result": (text,)}