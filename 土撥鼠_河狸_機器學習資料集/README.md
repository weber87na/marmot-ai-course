# Marmot / Beaver image dataset

Two-class image dataset collected from Wikimedia Commons for educational machine-learning experiments.

## Layout

- `marmot/`: 50 images
- `beaver/`: 50 images
- `metadata.csv`: source, creator, license, dimensions, and SHA-256 for every image

## Image format

Every image is an RGB JPEG at **224 × 224 pixels**. The original image was orientation-corrected, resized proportionally, and center-cropped to a square.

## Important note

This is a `marmot` versus `beaver` species-classification dataset. It is not, by itself, a real-versus-AI/fake detector dataset; that task also requires a separate, clearly labeled fake/AI-generated class.

## Attribution

The image source page and license metadata for each file are recorded in `metadata.csv`. Check each source page before redistribution or commercial use, and retain the required attribution for the listed license.

## Licenses found

- CC BY 2.0
- CC BY 2.5
- CC BY 3.0
- CC BY 4.0
- CC BY-SA 2.0
- CC BY-SA 2.5
- CC BY-SA 3.0
- CC BY-SA 3.0 nl
- CC BY-SA 4.0
- CC0
- Public domain
