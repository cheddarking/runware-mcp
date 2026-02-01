#!/usr/bin/env python3
"""
Real-ESRGAN Image Upscaling Helper Script

Usage:
    python upscale_image.py <input_path> [scale] [output_dir]

Arguments:
    input_path   Path to input image file (required)
    scale        Upscale factor: 2 or 4 (default: 2)
    output_dir   Output directory (default: input directory)

Examples:
    python upscale_image.py image.png
    python upscale_image.py image.png 4
    python upscale_image.py image.png 2 ./output
"""

import sys
import subprocess
from pathlib import Path


def upscale(input_path: str, scale: int = 2, output_dir: str = None, model: str = None):
    """
    Upscale an image using Real-ESRGAN

    Args:
        input_path: Path to input image
        scale: Scale factor (2 or 4)
        output_dir: Output directory (optional)
        model: Model name (optional, auto-selected based on scale)

    Returns:
        Path to output directory

    Raises:
        ValueError: If scale is not 2 or 4
        FileNotFoundError: If input file or Real-ESRGAN not found
        RuntimeError: If upscaling fails
    """

    # Validation
    if scale not in [2, 4]:
        raise ValueError(f"Scale must be 2 or 4, got: {scale}")

    input_path = Path(input_path).resolve()
    if not input_path.exists():
        raise FileNotFoundError(f"Input image not found: {input_path}")

    # Check Real-ESRGAN installation
    realesrgan_script = Path.home() / "Projects/Real-ESRGAN/inference_realesrgan.py"
    if not realesrgan_script.exists():
        raise FileNotFoundError(
            f"Real-ESRGAN not found at: {realesrgan_script}\n"
            "Please install Real-ESRGAN at ~/Projects/Real-ESRGAN"
        )

    # Determine model
    if model is None:
        model = f"RealESRGAN_x{scale}plus"

    # Set output directory
    if output_dir is None:
        output_dir = input_path.parent
    else:
        output_dir = Path(output_dir).resolve()
        output_dir.mkdir(parents=True, exist_ok=True)

    # Build command
    cmd = [
        "python3",
        str(realesrgan_script),
        "-n", model,
        "-i", str(input_path),
        "-o", str(output_dir),
        "-s", str(scale)
    ]

    print(f"Upscaling {input_path.name} with {scale}x scale...")
    print(f"Model: {model}")
    print(f"Output directory: {output_dir}")

    # Execute Real-ESRGAN
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            cwd=realesrgan_script.parent
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Upscaling failed with exit code {result.returncode}:\n"
                f"STDOUT: {result.stdout}\n"
                f"STDERR: {result.stderr}"
            )

        # Find output file
        # Real-ESRGAN adds _out suffix to filename
        output_name = input_path.stem + "_out" + input_path.suffix
        output_file = output_dir / output_name

        if output_file.exists():
            print(f"✅ Success! Upscaled image saved to: {output_file}")
            return str(output_file)
        else:
            print(f"⚠️  Upscaling completed but output file not found at expected location")
            print(f"   Expected: {output_file}")
            print(f"   Check output directory: {output_dir}")
            return str(output_dir)

    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Failed to execute Real-ESRGAN: {e}")


def main():
    """Command-line interface"""

    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print(__doc__)
        sys.exit(0 if len(sys.argv) == 1 else 0)

    # Parse arguments
    input_path = sys.argv[1]
    scale = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        result = upscale(input_path, scale, output_dir)
        print(f"\n📁 Output: {result}")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
