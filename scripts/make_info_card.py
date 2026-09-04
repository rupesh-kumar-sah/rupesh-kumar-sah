"""Generate the profile's terminal system-information card."""

from pathlib import Path

LINES = [
    ("OS", "Linux / Windows"),
    ("Host", "Kathmandu, Nepal"),
    ("Role", "Full-Stack & Backend Developer"),
    ("Stack", "PHP · Laravel · Python · Django"),
    ("Data", "MySQL · PostgreSQL · MongoDB"),
    ("Mobile", "React Native"),
    ("Socials", "LinkedIn · GitHub"),
    ("Web", "lexicon-books.onrender.com"),
    ("GitHub", "github.com/rupesh-kumar-sah"),
]


def write_card(output_path: Path) -> None:
    width, row_height = 620, 35
    height = 70 + len(LINES) * row_height
    rows = "\n".join(
        f'<g class="row" style="animation-delay:{index * 90}ms"><text x="28" y="{92 + index * row_height}" class="key">{key:<8}</text><text x="155" y="{92 + index * row_height}" class="value">{value}</text></g>'
        for index, (key, value) in enumerate(LINES)
    )
    output_path.write_text(
        f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img">
<title>The Cipher Stack profile information</title>
<rect width="100%" height="100%" rx="14" fill="#0d0d0d" stroke="#D4AF37" stroke-width="2"/>
<circle cx="24" cy="25" r="6" fill="#ff5f56"/><circle cx="44" cy="25" r="6" fill="#ffbd2e"/><circle cx="64" cy="25" r="6" fill="#27c93f"/>
<text x="90" y="30" fill="#D4AF37" font-family="monospace" font-size="16">The Cipher Stack</text>
<line x1="24" y1="52" x2="{width - 24}" y2="52" stroke="#343434"/>
{rows}
<style>.row{{opacity:0;animation:fade .55s ease-out forwards}}.key{{fill:#D4AF37;font:bold 15px monospace}}.value{{fill:#d6d6d6;font:15px monospace}}@keyframes fade{{to{{opacity:1;transform:translateX(4px)}}}}</style>
</svg>
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    write_card(Path("info-card.svg"))
