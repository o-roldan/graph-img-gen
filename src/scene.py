from manim import *
from src.graph_utils import load_cora, get_layouts


class CommunityTransitionObvious(Scene):
    def construct(self):
        # 1. Cargar datos
        G = load_cora("data/super_obvious_communities.graphml")

        # TIP DE DESARROLLO: Para hacer pruebas rápidas de video, descomenta la siguiente línea.
        # Renderizar 2,700 nodos toma tiempo. Prueba con 300 nodos primero.
        # G = G.subgraph(list(G.nodes)[:300])

        pos_random, pos_spring = get_layouts(G)

        # 2. Configurar la estética de nodos y aristas
        vertex_config = {}
        for node in G.nodes():
            vertex_config[node] = {
                "radius": 0.04,
                "color": BLACK,
                "fill_opacity": 0.85,
                "stroke_width": 0.3,
                "stroke_color": BLACK
            }

        edge_config = {
            "stroke_width": 0.1,
            "stroke_opacity": 0.75,
            "color": DARK_GRAY
        }

        # 4. Construir el objeto Graph de Manim
        print("Construyendo el objeto visual...")
        m_graph = Graph(
            list(G.nodes()),
            list(G.edges()),
            layout=pos_random,
            vertex_config=vertex_config,
            edge_config=edge_config
        )

        # 5. Secuencia de Animación
        self.add(m_graph)  # Mostrar estado caótico
        self.wait(1)      # Pausa de 1 segundo

        # Magia: Mover nodos a sus posiciones de comunidad
        self.play(
            m_graph.animate.change_layout(pos_spring),
            run_time=4.5,     # 1.5s más rápido
            rate_func=smooth  # Aceleración y desaceleración suave
        )

        # Recolorear al final cuando las comunidades ya estan agrupadas
        colors = [RED, BLUE, GREEN, YELLOW, ORANGE, TEAL, PURPLE]
        self.play(
            AnimationGroup(
                *[
                    m_graph.vertices[node].animate.set_fill(
                        colors[int(G.nodes[node].get("community", 0)) % len(colors)],
                        opacity=0.9,
                    )
                    for node in G.nodes()
                ],
                lag_ratio=0.0,
            ),
            run_time=1.0,
            rate_func=smooth,
        )

        self.wait(2)  # Pausa final antes de que acabe el video
