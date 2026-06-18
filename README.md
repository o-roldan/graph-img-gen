# graph-img-gen

Turn a graph into a slide-ready animation: nodes start as a random "cloud" and
smoothly relax into clearly separated, color-coded communities. A clean, reusable
way to *show* what clustering / community detection does — instead of explaining
it with a static bullet point.

Output is a 1080p / 60fps MP4 you drop straight onto a slide.

## Quick start

```bash
uv sync

# render the animation (high quality)
uv run manim render -qh src/scene.py CommunityTransitionObvious
```

The MP4 lands in `media/videos/scene/<resolution>/`.

Quality flags: `-ql` (low, fast preview) · `-qm` (medium) · `-qh` (high).

## Use your own graph

Any GraphML file works. Point the scene at it by editing the path in
`src/scene.py`:

```python
G = load_cora("data/super_obvious_communities.graphml")
```

A few ready-to-render graphs are included (`simple_20_nodes`, `sparse_100_nodes`,
`super_obvious_communities`, `cora`, …). Nodes are grouped/colored by their
`community` attribute.

To regenerate the Cora citation graph from scratch:

```bash
uv run python main.py   # writes cora.graphml
```

**Tip:** large graphs render slowly. Uncomment the `G.subgraph(...)` line in
`src/scene.py` to preview with fewer nodes first.
