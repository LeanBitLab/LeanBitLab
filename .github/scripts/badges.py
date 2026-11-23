"""Local SVG badges (no shields.io).

Repo stats pills and label buttons use the same solid look as the Official Website button:
dark fill with white text on light themes, light fill with dark text on dark themes
(prefers-color-scheme). Support buttons are colored on purpose so they stand out.
Run `python3 .github/scripts/badges.py` to (re)create the static buttons.
"""
import os
import re

FONT = "font-family=\"'Segoe UI', Ubuntu, Roboto, sans-serif\""
# GitHub switches <picture> sources by the viewer's GitHub theme, while an SVG's own
# prefers-color-scheme follows the OS, so every themed image is written as a -light and a -dark file.
PALETTE = {
    "light": {"bg": "#1f2328", "fg": "#ffffff", "rule": "#ffffff", "lb": "#1f2328", "vb": "#424a53", "tx": "#ffffff"},
    "dark": {"bg": "#f0f6fc", "fg": "#1f2328", "rule": "#1f2328", "lb": "#f0f6fc", "vb": "#c9d1d9", "tx": "#1f2328"},
}
THEMES = ("light", "dark")
_OPPOSITE = {"light": "dark", "dark": "light"}  # table badges use the opposite palette (light badges on light pages, dark on dark)


def _style(theme):
    c = PALETTE[theme]
    return ("  <style>\n" + "".join(f"    .{k} {{ fill: {v}; }}\n" for k, v in c.items())
            + f"    .rule {{ stroke: {c['rule']}; stroke-opacity: 0.25; }}\n  </style>")


STAR = (16, 16, "M8 0L10.472 5.008L16 5.816L12 9.712L12.944 15.216L8 12.616L3.056 15.216L4 9.712L0 5.816L5.528 5.008L8 0Z")
DOWN = (16, 16, "M8 12L3 7H6V0H10V7H13L8 12ZM0 14H16V16H0V14Z")

ICONS = {  # (width, height, path); Font Awesome Free brand icons (CC BY 4.0), X and Open Collective drawn by hand
    "discord": (448, 512, "M297.216 243.2c0 15.616-11.52 28.416-26.112 28.416-14.336 0-26.112-12.8-26.112-28.416s11.52-28.416 26.112-28.416c14.592 0 26.112 12.8 26.112 28.416zm-119.552-28.416c-14.592 0-26.112 12.8-26.112 28.416s11.776 28.416 26.112 28.416c14.592 0 26.112-12.8 26.112-28.416.256-15.616-11.52-28.416-26.112-28.416zM448 52.736V512c-64.494-56.994-43.868-38.128-118.784-107.776l13.568 47.36H52.48C23.552 451.584 0 428.032 0 398.848V52.736C0 23.552 23.552 0 52.48 0h343.04C424.448 0 448 23.552 448 52.736zm-72.96 242.688c0-82.432-36.864-149.248-36.864-149.248-36.864-27.648-71.936-26.88-71.936-26.88l-3.584 4.096c43.52 13.312 63.744 32.512 63.744 32.512-60.811-33.329-132.244-33.335-191.232-7.424-9.472 4.352-15.104 7.424-15.104 7.424s21.248-20.224 67.328-33.536l-2.56-3.072s-35.072-.768-71.936 26.88c0 0-36.864 66.816-36.864 149.248 0 0 21.504 37.12 78.08 38.912 0 0 9.472-11.52 17.152-21.248-32.512-9.728-44.8-30.208-44.8-30.208 3.766 2.636 9.976 6.053 10.496 6.4 43.21 24.198 104.588 32.126 159.744 8.96 8.96-3.328 18.944-8.192 29.44-15.104 0 0-12.8 20.992-46.336 30.464 7.68 9.728 16.896 20.736 16.896 20.736 56.576-1.792 78.336-38.912 78.336-38.912z"),
    "telegram": (496, 512, "M248 8C111 8 0 119 0 256s111 248 248 248 248-111 248-248S385 8 248 8zm121.8 169.9l-40.7 191.8c-3 13.6-11.1 16.9-22.4 10.5l-62-45.7-29.9 28.8c-3.3 3.3-6.1 6.1-12.5 6.1l4.4-63.1 114.9-103.8c5-4.4-1.1-6.9-7.7-2.5l-142 89.4-61.2-19.1c-13.3-4.2-13.6-13.3 2.8-19.7l239.1-92.2c11.1-4 20.8 2.7 17.2 19.5z"),
    "youtube": (576, 512, "M549.655 124.083c-6.281-23.65-24.787-42.276-48.284-48.597C458.781 64 288 64 288 64S117.22 64 74.629 75.486c-23.497 6.322-42.003 24.947-48.284 48.597-11.412 42.867-11.412 132.305-11.412 132.305s0 89.438 11.412 132.305c6.281 23.65 24.787 41.5 48.284 47.821C117.22 448 288 448 288 448s170.78 0 213.371-11.486c23.497-6.321 42.003-24.171 48.284-47.821 11.412-42.867 11.412-132.305 11.412-132.305s0-89.438-11.412-132.305zm-317.51 213.508V175.185l142.739 81.205-142.739 81.201z"),
    "reddit": (512, 512, "M440.3 203.5c-15 0-28.2 6.2-37.9 15.9-35.7-24.7-83.8-40.6-137.1-42.3L293 52.3l88.2 19.8c0 21.6 17.6 39.2 39.2 39.2 22 0 39.7-18.1 39.7-39.7s-17.6-39.7-39.7-39.7c-15.4 0-28.7 9.3-35.3 22l-97.4-21.6c-4.9-1.3-9.7 2.2-11 7.1L246.3 177c-52.9 2.2-100.5 18.1-136.3 42.8-9.7-10.1-23.4-16.3-38.4-16.3-55.6 0-73.8 74.6-22.9 100.1-1.8 7.9-2.6 16.3-2.6 24.7 0 83.8 94.4 151.7 210.3 151.7 116.4 0 210.8-67.9 210.8-151.7 0-8.4-.9-17.2-3.1-25.1 49.9-25.6 31.5-99.7-23.8-99.7zM129.4 308.9c0-22 17.6-39.7 39.7-39.7 21.6 0 39.2 17.6 39.2 39.7 0 21.6-17.6 39.2-39.2 39.2-22 .1-39.7-17.6-39.7-39.2zm214.3 93.5c-36.4 36.4-139.1 36.4-175.5 0-4-3.5-4-9.7 0-13.7 3.5-3.5 9.7-3.5 13.2 0 27.8 28.5 120 29 149 0 3.5-3.5 9.7-3.5 13.2 0 4.1 4 4.1 10.2.1 13.7zm-.8-54.2c-21.6 0-39.2-17.6-39.2-39.2 0-22 17.6-39.7 39.2-39.7 22 0 39.7 17.6 39.7 39.7-.1 21.5-17.7 39.2-39.7 39.2z"),
    "heart": (512, 512, "M462.3 62.6C407.5 15.9 326 24.3 275.7 76.2L256 96.5l-19.7-20.3C186.1 24.3 104.5 15.9 49.7 62.6c-62.8 53.6-66.1 149.8-9.9 207.9l193.5 199.8c12.5 12.9 32.8 12.9 45.3 0l193.5-199.8c56.3-58.1 53-154.3-9.8-207.9z"),
    "globe": (16, 16, "M8 0a8 8 0 1 0 0 16A8 8 0 0 0 8 0zm5.9 7.2h-2.8a11.8 11.8 0 0 0-1.1-4A6.4 6.4 0 0 1 13.9 7.2zM8 1.6c.8 1.3 1.3 3.2 1.5 5.6h-3C6.7 4.8 7.2 2.9 8 1.6zM2.1 7.2A6.4 6.4 0 0 1 6 3.2a11.8 11.8 0 0 0-1.1 4zm0 1.6h2.8c.2 1.5.5 2.8 1.1 4a6.4 6.4 0 0 1-3.9-4zm4.4 0h3c-.2 2.4-.7 4.3-1.5 5.6-.8-1.3-1.3-3.2-1.5-5.6zm3.5 4c.6-1.2.9-2.5 1.1-4h2.8a6.4 6.4 0 0 1-3.9 4z"),
    "x": (24, 24, "M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"),
    "opencollective": (24, 24, "M12 1.5a10.5 10.5 0 1 0 8.9 16l-3.8-2.4A6 6 0 1 1 18 12h4.5A10.5 10.5 0 0 0 12 1.5z"),
}


def _text_width(text, per_char=6.4):
    return len(text) * per_char


def _icon(icon, x, y, size, cls="fg", fill=None):
    """SVG <path> for an icon scaled to `size` px tall at (x, y); returns (markup, width)."""
    w, h, d = icon
    scale = size / h
    color = f' fill="{fill}"' if fill else f' class="{cls}"'
    return f'  <path{color} transform="translate({x:.1f} {y:.1f}) scale({scale:.4f})" d="{d}"/>', w * scale


def repo_badge_svg(version, stars_text, downloads_text, theme="light", max_row=232):
    """Flat two-tone badges (label | value) like the old shields look, packed into rows.

    Black label/value with white text on light themes, white with dark text on dark themes.
    """
    h, gap, font, per = 22, 6, 11, 6.7
    items = []
    if version:
        items.append(("Version", version))
    items.append(("Stars", stars_text))
    if downloads_text:
        items.append(("Downloads", downloads_text))
    sized = []
    for label, value in items:
        lw = round(_text_width(label, per) + 16)
        vw = round(_text_width(value, per) + 16)
        sized.append((label, value, lw, vw))
    rows, cur, cur_w = [], [], 0
    for it in sized:
        w = it[2] + it[3]
        if cur and cur_w + gap + w > max_row:
            rows.append(cur)
            cur, cur_w = [], 0
        cur.append(it)
        cur_w += (gap if len(cur) > 1 else 0) + w
    rows.append(cur)
    width = max(sum(i[2] + i[3] for i in r) + gap * (len(r) - 1) for r in rows)
    height = len(rows) * h + (len(rows) - 1) * gap
    parts = []
    for ri, row in enumerate(rows):
        y, x = ri * (h + gap), 0
        for label, value, lw, vw in row:
            parts.append(f'  <rect class="lb" x="{x}" y="{y}" width="{lw}" height="{h}" rx="3"/>')
            parts.append(f'  <rect class="vb" x="{x + lw}" y="{y}" width="{vw}" height="{h}" rx="3"/>')
            parts.append(f'  <rect class="vb" x="{x + lw}" y="{y}" width="6" height="{h}"/>')
            parts.append(f'  <rect class="lb" x="{x + lw - 6}" y="{y}" width="6" height="{h}"/>')
            parts.append(f'  <text class="tx" x="{x + lw / 2:.1f}" y="{y + 15}" text-anchor="middle" font-size="{font}" font-weight="600" {FONT}>{label}</text>')
            parts.append(f'  <text class="tx" x="{x + lw + vw / 2:.1f}" y="{y + 15}" text-anchor="middle" font-size="{font}" font-weight="700" {FONT}>{value}</text>')
            x += lw + vw + gap
    body = "\n".join(parts)
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
            f'{_style(_OPPOSITE[theme])}\n{body}\n</svg>\n')


def button_svg(label, icon_key=None, height=36, font_size=13, color=None, theme="light"):
    """Solid mono button (same look as the Official Website button) with an optional brand icon."""
    icon_size = round(height * 0.44)
    icon_w = 0.0
    if icon_key:
        w, h, _ = ICONS[icon_key]
        icon_w = w * icon_size / h
    gap = 9 if icon_key else 0
    text_w = _text_width(label, font_size * 0.58)
    width = round(icon_w + gap + text_w + 44)
    x0 = (width - (icon_w + gap + text_w)) / 2
    parts = []
    if icon_key:
        markup, _ = _icon(ICONS[icon_key], x0, (height - icon_size) / 2, icon_size, fill="#ffffff" if color else None)
        parts.append(markup)
    text_attr = 'fill="#ffffff"' if color else 'class="fg"'
    parts.append(f'  <text {text_attr} x="{x0 + icon_w + gap:.1f}" y="{height / 2 + font_size * 0.36:.1f}" font-size="{font_size}" font-weight="600" {FONT}>{label}</text>')
    body = "\n".join(parts)
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
            f'{_style(theme)}\n  <rect {"fill=" + chr(34) + color + chr(34) if color else "class=" + chr(34) + "bg" + chr(34)} width="{width}" height="{height}" rx="{height // 4}"/>\n' + "\n".join(parts) + '\n</svg>\n')


def support_button_svg(label, icon_key, c1, c2, gid):
    """Colored, larger button for the support section (meant to be noticed)."""
    height, icon_size, font_size = 46, 20, 15
    w, h, _ = ICONS[icon_key]
    icon_w = w * icon_size / h
    gap = 10
    text_w = _text_width(label, font_size * 0.6)
    width = round(icon_w + gap + text_w + 56)
    x0 = (width - (icon_w + gap + text_w)) / 2
    markup, _ = _icon(ICONS[icon_key], x0, (height - icon_size) / 2, icon_size, fill="#ffffff")
    return (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
            f'  <defs><linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>\n'
            f'  <rect width="{width}" height="{height}" rx="12" fill="url(#{gid})"/>\n'
            f'  <rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="11.5" stroke="#ffffff" stroke-opacity="0.22"/>\n'
            f'{markup}\n'
            f'  <text x="{x0 + icon_w + gap:.1f}" y="{height / 2 + font_size * 0.36:.1f}" fill="#ffffff" font-size="{font_size}" font-weight="700" {FONT}>{label}</text>\n</svg>\n')


def safe_name(repo_name):
    return re.sub(r"[^a-z0-9_.-]", "-", repo_name.lower())


def repo_status_svg(label, theme="light"):
    h = 22
    lw, vw = round(_text_width("Status", 6.7) + 16), round(_text_width(label, 6.7) + 16)
    width = lw + vw
    return (f'<svg width="{width}" height="{h}" viewBox="0 0 {width} {h}" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
            f'{_style(_OPPOSITE[theme])}\n'
            f'  <rect class="lb" width="{lw}" height="{h}" rx="3"/>\n  <rect class="vb" x="{lw}" width="{vw}" height="{h}" rx="3"/>\n'
            f'  <rect class="vb" x="{lw}" width="6" height="{h}"/>\n  <rect class="lb" x="{lw - 6}" width="6" height="{h}"/>\n'
            f'  <text class="tx" x="{lw / 2:.1f}" y="15" text-anchor="middle" font-size="11" font-weight="600" {FONT}>Status</text>\n'
            f'  <text class="tx" x="{lw + vw / 2:.1f}" y="15" text-anchor="middle" font-size="11" font-weight="700" {FONT}>{label}</text>\n</svg>\n')


def sponsor_us_svg(theme="light"):
    """Outlined 'Sponsor Us' button with a pink heart."""
    c = PALETTE[theme]["bg"]
    w, h, d = ICONS["heart"]
    size = 16
    scale = size / h
    return ('<svg width="170" height="40" viewBox="0 0 170 40" fill="none" xmlns="http://www.w3.org/2000/svg">\n'
            f'  <rect x="0.75" y="0.75" width="168.5" height="38.5" rx="9.25" stroke="{c}" stroke-width="1.5"/>\n'
            f'  <path fill="#DB61A2" transform="translate({40 - (w * scale - size) / 2:.1f} 12) scale({scale:.4f})" d="{d}"/>\n'
            f'  <text x="64" y="24.5" fill="{c}" font-size="13" font-weight="600" {FONT}>Sponsor Us</text>\n</svg>\n')


def write_repo_badges(out_dir, fname, version, stars_text, downloads_text):
    for theme in THEMES:
        with open(os.path.join(out_dir, f"{fname}-{theme}.svg"), "w", encoding="utf-8") as f:
            f.write(repo_badge_svg(version, stars_text, downloads_text, theme))


def build_static():
    """File name (without .svg) -> SVG markup for the static buttons."""
    files = {
        "sponsor-github": support_button_svg("Sponsor on GitHub", "heart", "#EA4C89", "#BF3989", "gSponsor"),
        "sponsor-opencollective": support_button_svg("Open Collective", "opencollective", "#4C8DF6", "#2972F4", "gOc"),
        "social-discord": button_svg("Discord", "discord", color="#5865F2"),
        "social-telegram": button_svg("Telegram", "telegram", color="#2CA5E0"),
        "social-youtube": button_svg("YouTube", "youtube", color="#FF0000"),
        "social-reddit": button_svg("Reddit", "reddit", color="#FF4500"),
    }
    for theme in THEMES:
        files[f"status-in-development-{theme}"] = repo_status_svg("In Development", theme)
        files[f"social-x-{theme}"] = button_svg("X", "x", theme=theme)
        files[f"website-{theme}"] = button_svg("Official Website", "globe", height=40, theme=theme)
        files[f"sponsor-us-{theme}"] = sponsor_us_svg(theme)
    return files


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "badges")
    os.makedirs(out, exist_ok=True)
    files = build_static()
    for name, svg in files.items():
        with open(os.path.join(out, f"{name}.svg"), "w", encoding="utf-8") as f:
            f.write(svg)
    print(f"Wrote {len(files)} static badges")
