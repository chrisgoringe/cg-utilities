from .common import Base_utilities
   
class Inspect(Base_utilities):
    CATEGORY = "utilities/developer"
    OPTIONAL = { "anything": ("*",{}) }
    OUTPUT_NODE = True

    def func(cls, anything=None):
        pass # put breakpoint here
        return()
