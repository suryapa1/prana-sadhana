# Prana Sadhana

A guided daily practice of about 28 minutes. It runs in any browser, with no install, account or server.

1. Arrive (settle the body and breath)
2. Opening Om, chanted 3 times along with a synthesized tone
3. Deep breathing: 20 counted rounds, 5 s in and 20 s out
4. Anulom Vilom: 15 rounds of alternate nostril breathing
5. Silent meditation: 10 minutes, with bells at halfway and at the end
6. Closing: Om 3 times, then Shanti

## Languages and scripted text

Every spoken and on-screen line comes from a fixed transcript file:

| File | Language | Speech voice |
|---|---|---|
| `transcripts/en.json` | English | en-IN, or any English voice |
| `transcripts/hi.json` | हिन्दी | hi-IN |
| `transcripts/te.json` | తెలుగు | te-IN |

No text is generated at runtime. The only variable parts are numbers filled into `{placeholders}` (round number, counts, minutes). Step durations are fixed in seconds in `src/app.html` (`buildPhases`) and are the same for every language. Spoken instructions may hold for up to 12 s so a sentence is never cut off.

The voice is the device's own text-to-speech. Hindi voices are on most Android, iOS and desktop Chrome. A Telugu voice is on Android (Google TTS) and some desktops. If the device has no voice for the chosen language, the app shows the text on screen and plays chimes, and never reads the script in the wrong language.

### Adding a language
1. Copy `transcripts/en.json` to `transcripts/<code>.json` (for example `ta.json`) and translate every value. Keep the `{placeholders}`.
2. Set `meta.code`, `meta.name`, `meta.englishName` and `meta.speechLang` (for example `ta-IN`).
3. Run `python3 build.py`. The build fails and lists any key that is missing or any placeholder that differs.

## Build

```bash
python3 build.py
```

This writes `index.html` (the full page for static hosting) and `dist/artifact.html` (the claude.ai artifact version, not committed).

## Hosting

`index.html`, `manifest.webmanifest`, `sw.js` and the icons are a static site that can be installed and works offline. It can be put on GitHub Pages, Cloudflare Pages, Netlify or any web server. On a phone, open the site and choose **Add to Home Screen**.
