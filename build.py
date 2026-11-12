#!/usr/bin/env python3
"""Build Prana Sadhana from src/app.html + transcripts/*.json.

The transcripts are the single source of truth for every spoken and on-screen
line. The build refuses to run if any language is missing a key that English
has, or uses a different set of {placeholders}, so every language plays the
exact same session.

Outputs:
  index.html            full page for GitHub Pages / any static host
  dist/artifact.html    page fragment for the claude.ai artifact
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).parent
PH = re.compile(r"\{(\w+)\}")


def flatten(d, prefix=""):
    for k, v in d.items():
        key = f"{prefix}{k}"
        if isinstance(v, dict):
            yield from flatten(v, key + ".")
        else:
            yield key, v


def load():
    files = sorted((ROOT / "transcripts").glob("*.json"))
    tx = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in files}
    if "en" not in tx:
        sys.exit("transcripts/en.json is required as the reference language")
    ref = dict(flatten(tx["en"]))
    errors = []
    for code, data in tx.items():
        if data["meta"]["code"] != code:
            errors.append(f"{code}: meta.code is {data['meta']['code']!r}")
        flat = dict(flatten(data))
        for k, v in ref.items():
            if k.startswith("meta."):
                continue
            if k not in flat:
                errors.append(f"{code}: missing {k}")
            elif set(PH.findall(str(v))) != set(PH.findall(str(flat[k]))):
                errors.append(f"{code}: placeholders differ in {k}")
        for k in flat:
            if k not in ref:
                errors.append(f"{code}: extra key {k} (not in en)")
    if errors:
        sys.exit("Transcript check failed:\n  " + "\n  ".join(errors))
    order = ["en"] + [c for c in tx if c != "en"]
    return {c: tx[c] for c in order}


def main():
    tx = load()
    blob = json.dumps(tx, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    tag = f'<script type="application/json" id="transcripts">{blob}</script>'
    src = (ROOT / "src" / "app.html").read_text(encoding="utf-8")
    if "<!--TRANSCRIPTS-->" not in src:
        sys.exit("src/app.html is missing the <!--TRANSCRIPTS--> marker")
    body = src.replace("<!--TRANSCRIPTS-->", tag)

    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "artifact.html").write_text(body, encoding="utf-8")

    head_extra = (
        '<meta name="description" content="A guided daily breathing and meditation practice with Om chanting, in English, Hindi and Telugu.">\n'
        '<meta name="theme-color" content="#0f1329">\n'
        '<link rel="manifest" href="manifest.webmanifest">\n'
        '<link rel="icon" href="icon.svg" type="image/svg+xml">\n'
        '<link rel="apple-touch-icon" href="icon-192.png">\n'
        '<meta name="apple-mobile-web-app-capable" content="yes">\n'
    )
    sw = (
        "<script>if('serviceWorker' in navigator && location.protocol==='https:'){"
        "navigator.serviceWorker.register('sw.js').catch(function(){});}</script>\n"
    )
    page = (
        "<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        + head_extra
        + "<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}"
        "body{margin:0}[hidden]{display:none!important}img{max-width:100%}</style>\n"
        "</head>\n<body>\n" + body + "\n" + sw + "</body>\n</html>\n"
    )
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    langs = ", ".join(f"{c} ({d['meta']['englishName']}, {len(d['lines'])} lines)" for c, d in tx.items())
    print(f"Built index.html and dist/artifact.html with {langs}")


if __name__ == "__main__":
    main()
