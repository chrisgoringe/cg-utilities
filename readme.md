# CG's custom nodes: Utilities

[Index of my custom nodes](https://github.com/chrisgoringe/cg-nodes-index)

## Utilities

To install:
```
cd [path to ComfyUI]/custom_nodes
git clone https://github.com/chrisgoringe/cg-utilities.git
```

A set of nodes that I find really helpful in making clean workflows...

## utilities/conditioning

`Two Clip Text Encode` - one clip, two text strings, two conditioninings. For prompt and negative prompt.
`Merge Conditionings` - merge two conditionings based on a mask

## utilities/conversion

`To String|Int|Float` - take any input and try to convert it into the appropriate type.

## utilities/developer

`Inspect` - the simplest class of all time - takes any input, and does nothing. If you're a developer, put a breakpoint permanently at line 9 of utilitites_developer.py
and use this node to look at anything.

## utilities/images

`Image Size` - Get the size of an image

`Resize Image` - Resize an image. Does the following steps to calculate the new size:
- Takes the size of the incoming image, or the size of the **image_to_match** (if there is one)
- Multiplies by **factor** (default 1.0 does nothing)
- If resulting  height or width is larger than **max_dimension**, reduce them (preserving aspect ratio)
- if **x8** is 'yes' (the default), round height and width (independantly) to the nearest multiple of 8
The image is then rescaled (using torch.nn.functional.interpolate) to the new size. If there was an **image_to_match** it is also rescaled.

The result is two images (identical, if there was no **image_to_match**), equal to or smaller than **max_dimension** (or if **x8**, than the nearest multiple of 8 to **max_dimension**), and of identical sizes.

`Combine Images` - Combines up to four images (or lists of images) into a list of images.

`Mask Harden and Blur` - Takes a mask and sets it to 1 or 0 based on a threshold, then blurs the edges. Useful for recombining images.

## utilities/primitives

`String|Int|Float` - Primitive values 

## utilities/strings

`Show Text` - Take text input and display it in the UI. 

`Regex Substitution` - Takes a string input and does a regex substitution on it, returning the result and the number of substitutions made. Uses python `regex.sub()` [docs](https://docs.python.org/3/library/re.html)

`Substitute` - Takes a template and substitutes `[X]` and `[Y]` with the inputs, and `%date%` with `DD-MM-YYYY`

## utilities/passthrough     

Create a custom node based on any other node, with one or more of the inputs added as outputs. Look at `passthrough_config.json` for how do this (changes require a restart of ComfyUI and reload of the webpage):

```json
    "VAEEncodeForInpaintReturn" : {                             # a name unique in this file
        "display_name" : "VAE Encode For Inpaint Passthrough",  # The display name of the new custom node
        "based_on" : "VAEEncodeForInpaint",                     # The unique name of the node type you are basing it on
        "inputs_to_pass" : ["vae"],                             # A list of the names of the inputs to be added as outputs
        "category": null                                        # optionally, the custom node category (default is utilities/passthrough)
    },
```

`Passthrough Info` - shows the nodes that could be used for `based_on`

## Acknowledgements

I learned a lot from reading  [pythongosssss' Custom Scripts](https://github.com/pythongosssss/ComfyUI-Custom-Scripts), especially on how the javascript side of things works.