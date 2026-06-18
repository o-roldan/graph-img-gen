import networkx as nx
import numpy as np


def load_cora(filepath="data/super_obvious_communities.graphml"):
    """Carga el grafo exportado previamente."""
    G = nx.read_graphml(filepath)
    # Convertimos los IDs a enteros para facilitar el manejo
    G = nx.relabel_nodes(G, lambda x: int(x))

    # Compatibilidad: algunos GraphML traen la comunidad como modularity_class
    for _, data in G.nodes(data=True):
        if "community" not in data and "modularity_class" in data:
            data["community"] = int(data["modularity_class"])

    return G


def get_layouts(G):
    """Genera las coordenadas de inicio (aleatorio) y fin (agrupado visualmente)."""

    # 1. Estado Aleatorio
    pos_random = {}
    for node in G.nodes():
        pos_random[node] = np.array([
            np.random.uniform(-6, 6),
            np.random.uniform(-3.5, 3.5),
            0
        ])

    # 2. Estado Agrupado (Mejorado para Comunidades)
    print("Calculando centros de gravedad por comunidad...")

    # Identificar todas las comunidades únicas
    communities = {}
    for node, data in G.nodes(data=True):
        comm_id = data.get('community', 0)
        if comm_id not in communities:
            communities[comm_id] = []
        communities[comm_id].append(node)

    # Crear posiciones base (centros de masa) en forma circular para las comunidades
    # Aumentamos la escala para separarlas mejor visualmente
    centers = nx.circular_layout(list(communities.keys()), scale=5.0)

    # Asignar a cada nodo una posición inicial cerca de su centro de comunidad
    initial_pos = {}
    for comm_id, nodes in communities.items():
        center = centers[comm_id]
        for node in nodes:
            # Menos ruido inicial para que cada comunidad nazca mas compacta
            initial_pos[node] = center + np.random.uniform(-0.45, 0.45, 2)

    print("Aplicando físicas de atracción locales...")
    # Ejecutamos el spring_layout, pero usando nuestras posiciones agrupadas como punto de partida (pos=initial_pos)
    # Reducimos k (distancia óptima) para que los clústeres se mantengan densos
    pos_spring_2d = nx.spring_layout(
        G, pos=initial_pos, k=0.08, iterations=30, seed=42)

    # Adaptamos el layout 2D al formato 3D de Manim (Manim usa un canvas de ~14x8)
    pos_spring = {}
    for node, coords in pos_spring_2d.items():
        # Ajustamos las coordenadas X e Y para llenar bien la pantalla 16:9
        pos_spring[node] = np.array([coords[0] * 1.8, coords[1] * 1.2, 0])

    return pos_random, pos_spring
