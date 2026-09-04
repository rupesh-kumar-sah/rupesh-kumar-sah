"""Render a prepared image as an animated terminal-style ASCII SVG."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

from PIL import Image, ImageOps

RAMP = " .`:-=+*cs#%@"


def render_ascii(image_path: Path, columns: int) -> list[str]:
    image = Image.open(image_path).convert("L")
    rows = max(1, round(image.height / image.width * columns * 0.48))
    image = ImageOps.fit(image, (columns, rows), method=Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    return [
        "".join(RAMP[pixel * (len(RAMP) - 1) // 255] for pixel in pixels[row * columns : (row + 1) * columns])
        for row in range(rows)
    ]


def write_svg(lines: list[str], output_path: Path) -> None:
    line_height = 14
    width = 24 + max(map(len, lines), default=1) * 8
    height = 52 + len(lines) * line_height
    escaped = [html.escape(line).replace(" ", "&#160;") for line in lines]
    text = "\n".join(
        f'<text x="20" y="{48 + index * line_height}" class="line" style="animation-delay:{index * 45}ms">{line}</text>'
        for index, line in enumerate(escaped)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">
<title>Animated ASCII portrait</title>
<defs><clipPath id="wipe"><rect width="{width}" height="{height}"><animate attributeName="width" from="0" to="{width}" dur="2.4s" fill="freeze"/></rect></clipPath></defs>
<rect width="100%" height="100%" rx="14" fill="#0d0d0d" stroke="#D4AF37" stroke-width="2"/>
<circle cx="20" cy="20" r="5" fill="#ff5f56"/><circle cx="38" cy="20" r="5" fill="#ffbd2e"/><circle cx="56" cy="20" r="5" fill="#27c93f"/>
<text x="76" y="24" fill="#9b9b9b" font-family="monospace" font-size="11">portrait.render()</text>
<g clip-path="url(#wipe)" fill="#D4AF37" font-family="monospace" font-size="10" xml:space="preserve">{text}</g>
<style>.line{{opacity:0;animation:fin .5s ease-out forwards}}@keyframes fin{{to{{opacity:1}}}}</style>
</svg>
"""
    output_path.write_text(svg, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", type=Path, default=Path("source-prepped.png"))
    parser.add_argument("-o", "--output", type=Path, default=Path("hxni-ascii.svg"))
    parser.add_argument("--columns", type=int, default=72)
    args = parser.parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"{args.input} is missing; run prep_photo.py first.")
    write_svg(render_ascii(args.input, args.columns), args.output)


if __name__ == "__main__":
    main()
