import networkx as nx
from torch_geometric.datasets import Planetoid
from torch_geometric.utils import to_networkx

# 1. Load the Cora dataset
print("Downloading/Loading Cora...")
dataset = Planetoid(root='./data/Cora', name='Cora')
data = dataset[0]

# 2. Convert to an undirected NetworkX graph
print("Converting to NetworkX...")
G = to_networkx(data, to_undirected=True)

# 3. Inject the ground-truth classes as 'community' attributes
labels = data.y.numpy()
class_names = ['Theory', 'Reinforcement_Learning', 'Genetic_Algorithms',
               'Neural_Networks', 'Probabilistic_Methods',
               'Case_Based', 'Rule_Learning']

for i in range(data.num_nodes):
    G.nodes[i]['community'] = int(labels[i])
    G.nodes[i]['class_name'] = class_names[labels[i]]

# 4. Export for Gephi
output_file = "cora.graphml"
nx.write_graphml(G, output_file)
print(f"Graph exported successfully to {output_file}")
