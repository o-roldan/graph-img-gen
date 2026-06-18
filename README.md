# graph-img-gen

Generates short graph animations used as background/transition clips in slide decks.

The signature animation takes a graph drawn as a random "cloud" of nodes and
smoothly relaxes it into clearly separated communities, then recolors each node
by its community — a visual way to explain clustering / community detection on a
slide.

## What's inside

| File | What it does |
|------|--------------|
| `main.py` | Downloads the **Cora** citation dataset, converts it to an undirected NetworkX graph, tags each node with its ground-truth class as a `community` attribute, and exports it to `cora.graphml` (also openable in Gephi). |
| `src/scene.py` | Manim scene (`CommunityTransitionObvious`). Loads a GraphML file, lays the nodes out at random, animates them into a community spring layout, then fades in per-community colors. This is what produces the video. |
| `src/graph_utils.py` | Helpers: `load_cora()` reads a GraphML graph and normalizes node IDs/community labels; `get_layouts()` computes the random start layout and the clustered spring-layout end state. |
| `*.graphml` / `data/*.graphml` | Ready-to-render graphs of varying size (`simple_20_nodes`, `sparse_100_nodes`, `sparse_200_nodes`, `super_obvious_communities`, `cora`). |
| `gephi/community.gephi` | Gephi project for laying out / coloring graphs by hand. |
| `manim.cfg` | Render defaults: 1920×1080, 60 fps, white background. |

## Setup

Uses [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

## Usage

### Render the animation

```bash
# high quality (uses manim.cfg: 1080p / 60fps / white bg)
uv run manim render -qh src/scene.py CommunityTransitionObvious
```

Quality flags: `-ql` (low, fast iteration) · `-qm` (medium) · `-qh` (high). The
output MP4 lands in `media/videos/scene/<resolution>/`.

> **Tip:** rendering thousands of nodes is slow. While iterating, uncomment the
> `G.subgraph(...)` line in `src/scene.py` to render a small subset first.

Pick the input graph by editing the `load_cora("...")` path in `src/scene.py`
(swap in any of the `*.graphml` files for fewer/cleaner nodes).

### Regenerate the Cora graph

```bash
uv run python main.py   # writes cora.graphml
```

## Output

The rendered MP4 (16:9, 60 fps, white background) is meant to be dropped directly
onto a slide as a transition/animation clip.
