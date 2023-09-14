# CG's custom nodes: Utilities

[Index of my custom nodes](https://github.com/chrisgoringe/cg-nodes-index)

## Utilities

To install:
```
cd [path to ComfyUI]/custom_nodes
git clone https://github.com/chrisgoringe/cg-utilities.git
```

A set of nodes that I find really helpful in making clean workflows. Several of these nodes make use of my [core node code](https://github.com/chrisgoringe/cg-custom-core), which should be automatically installed when you first use the nodes (note that this may require ComfyUI to be restarted) if it isn't present.

## utilities/conditioning

`Two Clip Text Encode` - one clip, two text strings, two conditioninings. For prompt and negative prompt.

`Merge Conditionings` - merge two conditionings based on a mask

## utilities/conversion

`To String|Int|Float` - take any input and try to convert it into the appropriate type.

## utilities/developer

`Inspect` - the simplest class of all time - takes any input, and does nothing. If you're a developer, put a breakpoint permanently at line 9 of utilitites_developer.py
and use this node to look at anything.

`Combo Pass` - WIP. Suggest you don't use this.

## utilities/images

`Image Size` - Get the size of an image

`Resize Image` - Constrained resize of an image. The initial size is the size of *image_to_match*, if that (optional) input is connected, else the size of *image*. There are three constraint modes:
- `none` - the image is scaled by *factor*, and then scaled down if the resulting height or width is greater than *max_dimension*.
- `x8` - as for `none`, but the height and width are adjusted to be the nearest multiple of 8.
- `cn512` - rescale to a ControlNet-compatible size. The image is rescaled to make the shorter dimension equal to 512, and the longer dimension a multiple of 64, while keeping the aspect ratio as close to the original as possible.

Once a final size has been determined, the *image* and *image_to_match* (if any) are both rescaled to the same size.

`Combine Images` - Combines up to four images (or lists of images) into a list of images.

`Compare Images` - Pixel-size comparison of two images, outputting a greyscale image of the changes between them.

`Mask Harden and Blur` - Takes a mask and sets it to 1 or 0 based on a threshold, then blurs the edges. Useful for recombining images.

## utilities/primitives

`String|Int|Float` - Primitive values 

## utilities/strings

`Show Text` - Take text input and display it in the UI. 

`Regex Substitution` - Takes a string input and does a regex substitution on it, returning the result and the number of substitutions made. Uses python `regex.sub()` [docs](https://docs.python.org/3/library/re.html)

`Substitute` - Takes a template and substitutes `[X]` and `[Y]` with the inputs, and `%date%` with `DD-MM-YYYY`

## utilities/passthrough     

Create a custom node based on any other node, with one or more of the inputs added as outputs. Look at `passthrough_config.json` for how do this (changes require a restart of ComfyUI and reload of the webpage) - the example takes the `VAE Encode For Inpaint` node and adds an output, `vae`, which is a copy of the input of the same name. This can be useful for making workflows tidier! Note that widget inputs can be output - sometimes useful to reuse a seed, or use the name of a checkpoint or LoRA.

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