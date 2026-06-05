Skills are organized into bucket folders under `skills/`:

- `engineering/` — daily code work
- `productivity/` — daily non-code workflow tools
- `misc/` — kept around but rarely used
- `personal/` — tied to my own setup, not promoted
- `in-progress/` — drafts not yet ready to ship
- `deprecated/` — no longer used

Every skill in `engineering/`, `productivity/`, or `misc/` must have a reference in the top-level `README.md` and an entry in `.claude-plugin/plugin.json`. Skills in `personal/`, `in-progress/`, and `deprecated/` must not appear in either.

Each skill entry in the top-level `README.md` must link the skill name to its `SKILL.md`.

Each bucket folder has a `README.md` that lists every skill in the bucket with a one-line description, with the skill name linked to its `SKILL.md`.

Note: You need to run Python from the virtual environment located at `venv`.

## Plotly Rendering in VS Code Jupyter Notebooks

### Issue
When displaying Plotly interactive figures in a Jupyter notebook (`.ipynb`) inside VS Code, the following warning/error may appear:
`No renderer could be found for mimetype "application/vnd.plotly.v1+json", but one might be available on the Marketplace.`

### Cause
By default, Plotly attempts to output charts using the `plotly_mimetype` renderer (`application/vnd.plotly.v1+json` mimetype). The VS Code Jupyter editor cannot render this mimetype natively unless a specific Plotly notebook extension is installed in the VS Code environment.

### Solution
Force Plotly to output standard `text/html` (loading the Plotly.js library from a CDN) which VS Code can render natively without any extensions. Add the following setup code to the imports/setup cell of the notebook:
```python
import plotly.io as pio
pio.renderers.default = "notebook_connected"
```

