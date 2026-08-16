# AI QA Agent

Type test instructions in plain English — one per line — and watch them
compile into structured test steps in a live console view.

```
open youtube
click search bar
username: qa_tester
password: my-secret
click login button
```

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000

## Project structure

```
app.py              Flask routes: renders the UI, exposes POST /parse
parser.py           Turns instruction text into structured step dicts
templates/index.html Page markup
static/css/style.css Design system + layout
static/js/script.js  Live gutter numbers + animated console output
requirements.txt    Python dependencies
vercel.json          Vercel build/routing config
```

## Deploying to Vercel

1. Push this repo to GitHub.
2. Import it in Vercel — `requirements.txt` and `vercel.json` are already
   set up so Vercel knows to build `app.py` with `@vercel/python`.
3. Deploy. The `/parse` endpoint and static assets are routed automatically.

**Note:** this app only *parses* instructions into a list of labeled
steps — it does not drive a real browser. Running actual browser
automation (e.g. with Playwright) needs a long-running process, which
Vercel's serverless functions don't support. That would need a separate
backend (a small VM, Render, Railway, etc.) that this UI could call into.

## Recognized instruction verbs

| Verb        | Produces          |
|-------------|-------------------|
| `open`      | `OPEN PAGE`       |
| `click`     | `CLICK BUTTON`    |
| `username`  | `ENTER USERNAME`  |
| `password`  | `ENTER PASSWORD`  |
