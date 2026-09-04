"""Prepare a portrait for the terminal-style SVG renderer."""

from __future__ import annotations

import argparse
from pathlib import Path

import cv2
from PIL import Image
from rembg import remove


def prepare_photo(input_path: Path, output_path: Path, size: tuple[int, int]) -> None:
    source = Image.open(input_path).convert("RGBA")
    foreground = remove(source)
    foreground.save(output_path.with_name("_foreground.png"))
    image = cv2.imread(str(output_path.with_name("_foreground.png")), cv2.IMREAD_COLOR)
    if image is None:
        raise FileNotFoundError(f"Could not read portrait: {input_path}")

    # Keep the subject centered while producing a predictable canvas for ASCII output.
    height, width = image.shape[:2]
    target_width, target_height = size
    scale = max(target_width / width, target_height / height)
    resized = cv2.resize(image, (round(width * scale), round(height * scale)), interpolation=cv2.INTER_AREA)
    y = max((resized.shape[0] - target_height) // 2, 0)
    x = max((resized.shape[1] - target_width) // 2, 0)
    cropped = resized[y : y + target_height, x : x + target_width]

    lab = cv2.cvtColor(cropped, cv2.COLOR_BGR2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)
    enhanced = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8)).apply(l_channel)
    result = cv2.cvtColor(cv2.merge((enhanced, a_channel, b_channel)), cv2.COLOR_LAB2RGB)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(result).save(output_path)
    foreground_path = output_path.with_name("_foreground.png")
    if foreground_path.exists():
        foreground_path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Portrait image path")
    parser.add_argument("-o", "--output", type=Path, default=Path("source-prepped.png"))
    parser.add_argument("--width", type=int, default=96)
    parser.add_argument("--height", type=int, default=64)
    args = parser.parse_args()
    prepare_photo(args.input, args.output, (args.width, args.height))


if __name__ == "__main__":
    main()
