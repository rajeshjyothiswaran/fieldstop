# ƒieldstop — offline camera field guide (PWA)

An installable, **fully offline** field guide and plain-language setup advisor for your camera. Built to work with **zero signal in the field**. One app can hold **multiple camera systems** — pick the body from the switcher in the header.

Currently loaded: **FUJIFILM GFX100S II** (firmware 1.20, verified current as of July 2026).

## What it does
- **Ask** — describe the shot ("milky way over a mountain lake", "silky waterfall", "focus stack a foreground") and get a camera-ready setup: exact settings, why each one, the steps on the camera, and any hard "Watch" note. Runs entirely on-device — no live AI, no API key, no network.
- **Setups** — 22 one-tap starting points, weighted toward landscape, nature and nightscape work (Milky Way, star trails, tracked astro, aurora, moonlit, blue-hour blends, seascape, woodland, autumn, panorama, focus-stacking…).
- **Menu** — all 234 GFX100S II menu items exactly as they appear on the camera, with manual page numbers. A green dot means it's explained in plain language — tap it.
- **Learn** — 45 feature explanations, all 12 film simulations, and the firmware 1.20 change notes.

The advisor is a deterministic on-device matcher over a curated knowledge base built from your Owner's Manual (BL00005287-202 EN) and New Features Guide v1.20. It passed 22/22 plain-language routing tests across all genres.

---

## Put it on your phone (installable + offline)

A PWA needs to be served over HTTPS once; after the first load it works offline forever.

**GitHub Pages (recommended — matches your existing workflow):**
1. Create a new repo (e.g. `fieldstop`) and upload these files so `fieldstop.html` sits at the repo root. Commit.
2. **Settings → Pages → Source: Deploy from a branch → Branch `main`, folder `/ (root)` → Save.**
3. ~1 minute later it's live at `https://<you>.github.io/fieldstop/`. The included `index.html` redirects that root URL straight to the app.

Giving Fieldstop its own repo means no filename clash with your other projects — each repo is an isolated deployment. All paths here are relative and the manifest scope is `./`, so the sub-path URL works correctly.

**Netlify Drop (no account, for a quick throwaway):** go to https://app.netlify.com/drop and drag the whole folder on. Fine, but you don't need a second host if you're already on GitHub.

**Install to home screen:** iPhone (Safari) → Share → *Add to Home Screen*. Android (Chrome) → ⋮ → *Install app*. Launch once online so it caches; then it's fully offline and full-screen.

> Opening the file straight off disk previews the app but won't install or cache — the HTTPS step is what makes it a real installable PWA.

### Name and logo
The name is the clean word **Fieldstop** (used in the manifest, tab title, and install label) — chosen to stay distinct from the crowded "F-Stop" photography brands and to match a one-word domain/handle. The **logo** carries the f-stop wink instead: an italic ƒ with the middle "ield" shrunk, so the large glyphs read *ƒ…stop* while the word stays *Fieldstop*. It renders in the header and on the launch/redirect page; the app icon is the matching aperture iris.

---

## Adding another camera system
The whole point of the multi-system design: a new body is just a data file, not a new app.

1. Copy `build/build_data.py` and author a new system (film sims, scenarios, features, recipes, menu) the same way, emitting `assets/systems/<id>.js` — each module ends with `window.FIELDSTOP_SYSTEMS.push({...})`.
2. Add one line to `fieldstop.html`: `<script src="./assets/systems/<id>.js"></script>` (before `app.js`).
3. Add the same path to the `ASSETS` list in `fieldstop-sw.js` so it caches offline, and bump the cache name (`fieldstop-v1` → `v2`).

The header switcher and everything else updates automatically. Menu→feature "green dot" links use a Fuji-specific alias map in `app.js`; a different brand can get its own map there.


## Versioning & deploy (the `deploy.sh` workflow)
Fieldstop carries a single version number, shown in the app on the **Learn** tab. It lives in one place — the `<meta name="fieldstop-version">` tag in `fieldstop.html` — and the service worker's cache name is derived from it, so **bumping the version is what forces installed apps to refresh their offline cache**.

Deploy with the script instead of manual git commands:
```
./deploy.sh          # re-deploy at the current version
./deploy.sh 1.1.0    # set a new version, then deploy
```
It (1) writes the version into `fieldstop.html` and `fieldstop-sw.js` and **fails if they don't match** (parity gate), (2) copies a snapshot of the deployable site into `releases/v<version>/` (a local archive, gitignored — so versioned copies live here, not in Downloads), and (3) commits and pushes to GitHub Pages.

First time only, make it executable: `chmod +x deploy.sh` (or run it as `bash deploy.sh`).

## Files
```
index.html                  root redirect → fieldstop.html (for GitHub Pages)
fieldstop.html              app shell + views (entry point)
fieldstop.webmanifest       install metadata
fieldstop-sw.js             offline cache (cache-first); version in parity with the app
deploy.sh                   version-sync + snapshot + commit + push
releases/                   local per-version snapshots (gitignored)
assets/app.css              styles (instrument-panel theme)
assets/app.js               routing, advisor matcher, system switcher
assets/systems/gfx100sii.js the GFX100S II knowledge base (generated)
icons/                      app icons
build/build_data.py         regenerates the GFX100S II module
build/menu_tree.json        parsed menu tree (234 items)
```
Edit content in `build/build_data.py`, then run `python3 build/build_data.py` to regenerate the module. Don't hand-edit the generated file.

## Accuracy note
Settings are sensible, manual-grounded starting points — light and subjects vary, so confirm exposure on the histogram. Hard constraints (e.g. the electronic shutter blocks flash and caps ISO 80–12800; the trailing-time guide for 102MP astro) are called out in the "Watch" notes.
