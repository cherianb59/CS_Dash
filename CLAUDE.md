# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

An Australian Child Support formula calculator with two implementations:
- **`cs_dash.py`** — a Plotly Dash app (Python/Flask backend, served via `app.wsgi`)
- **`index.html`** — a standalone client-side HTML/JS version using Bootstrap, Chart.js and D3

## Running the app

```bash
# Dash version (dev mode, port 5000)
python cs_dash.py

# Static HTML version — open directly in browser
open index.html
```

The Dash app is deployed via Apache mod_wsgi using `app.wsgi`, which adds the virtualenv at `/home/chez/env` and the project root to `sys.path`, then exposes `server` as `application`.

## Architecture

### Formula logic (`cs_baseline.py`)
The core Australian Child Support formula. Key functions:
- `cs_baseline(...)` — main formula entry point; returns a dict with `liability` (positive = Parent A pays B) and intermediate workings
- `care_to_cost(care_pct)` — converts nights-of-care fraction to cost fraction via legislated lookup
- `coc_simple(income, kids_12l, kids_13p, ...)` — cost-of-children using the income band taper table
- `default_income_bands` / `default_tapers` — 2022 baseline parameters; tapers are keyed by `(age_group, num_kids)` where `age_group` is `"12l"`, `"13p"`, or `"mix"`

### Dash app (`cs_dash.py`)
- Single-page layout with a **Calculator** tab (just the liability statement) and a **Model** tab (adds income-sweep charts and formula-parameter editors)
- One server-side callback (`update_liability_statement`) recalculates everything on any input change; the Model tab chart loop iterates income 0–300k in $1k steps
- Two `clientside_callback`s written in JS handle tab/child visibility toggling via `Utils.addCSSClass` / `Utils.removeCSSClass` (defined in `assets/Utils.js`) — these manipulate `className` rather than `style` so they avoid a server round-trip
- Parent A's care nights are sliders; Parent B's care nights are hardcoded to `[0,0,0,0,0]` (assumed zero nights in the current case)

### Static HTML version (`index.html`)
Self-contained page with the same formula reimplemented in JavaScript. Uses Bootstrap dark theme, Chart.js for charts, and D3 for any data manipulation. The formula JS mirrors `cs_baseline.py`.

### CSS class toggling pattern
Both Python (`utils/utils.py`) and JS (`assets/Utils.js`) expose matching `add/removeCSSClass` helpers. Elements are hidden with the `hidden` class (`display: none`). The Dash clientside callbacks pass `className` strings through these helpers to show/hide rows without re-rendering.
