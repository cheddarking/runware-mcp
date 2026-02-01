---
name: upscale-image
description: Upscale low-resolution images using Real-ESRGAN (2x or 4x). Use when users want to increase image resolution, sharpen blurry images, or "enhance" photos.
---

# Upscale Image

## Usage

This skill uses a Python script to upscale images using the Real-ESRGAN machine learning model. It supports 2x and 4x upscaling.

### Command

```bash
python3 <path-to-skill>/scripts/upscale_image.py <input_path> [scale] [output_dir]
```

### Parameters

- `input_path`: (Required) Path to the image file to upscale.
- `scale`: (Optional) Upscaling factor. Must be `2` or `4`. Defaults to `2`.
- `output_dir`: (Optional) Directory to save the upscaled image. Defaults to the same directory as the input image.

### Examples

**Upscale an image by 2x (default):**
```bash
python3 <path-to-skill>/scripts/upscale_image.py "images/photo.jpg"
```

**Upscale an image by 4x:**
```bash
python3 <path-to-skill>/scripts/upscale_image.py "images/photo.jpg" 4
```

**Upscale and save to a specific directory:**
```bash
python3 <path-to-skill>/scripts/upscale_image.py "images/photo.jpg" 4 "upscaled_images/"
```

## Troubleshooting

- **FileNotFoundError**: Ensure the input image path is correct and accessible.
- **Real-ESRGAN not found**: The script expects Real-ESRGAN to be installed at `~/Projects/Real-ESRGAN`. If it's elsewhere, you may need to update the script path.
- **Memory Errors**: 4x upscaling on large images can consume significant GPU VRAM or system RAM. Try 2x if 4x fails.