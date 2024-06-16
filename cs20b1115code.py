import random
import networkx as nx
import plotly.graph_objects as go

# Take input for the number of houses, malls, and petrol banks
num_houses = int(input("Enter the number of houses: "))
num_malls = int(input("Enter the number of malls: "))
num_petrol_banks = int(input("Enter the number of petrol banks: "))

# Create a graph representation of the city
G = nx.Graph()
locations = ['house{}'.format(i) for i in range(1, num_houses+1)] + ['mall{}'.format(i) for i in range(1, num_malls+1)] + ['petrol{}'.format(i) for i in range(1, num_petrol_banks+1)]

# Add nodes to the graph
for loc in locations:
    G.add_node(loc)

# Add edges between houses and malls/petrol stations
for house in range(1, num_houses+1):
    for i in range(1, num_malls+1):
        distance = random.randint(1, 10)
        G.add_edge('house{}'.format(house), 'mall{}'.format(i), weight=distance)
        print(f"Distance from house{house} to mall{i}: {distance}")
    for i in range(1, num_petrol_banks+1):
        distance = random.randint(1, 10)
        G.add_edge('house{}'.format(house), 'petrol{}'.format(i), weight=distance)
        print(f"Distance from house{house} to petrol{i}: {distance}")

# Add edges between petrol stations and malls
for i in range(1, num_petrol_banks+1):
    for j in range(1, num_malls+1):
        distance = random.randint(1, 10)
        G.add_edge('petrol{}'.format(i), 'mall{}'.format(j), weight=distance)
        print(f"Distance from petrol{i} to mall{j}: {distance}")

# Take input for the starting and ending locations
source = input("Enter the starting location: ")
while source not in locations:
    source = input("Invalid location. Enter the starting location: ")
target = input("Enter the ending location: ")
while target not in locations:
    target = input("Invalid location. Enter the ending location: ")

# Find the shortest path between the starting and ending locations using A* algorithm
shortest_path = nx.astar_path(G, source=source, target=target, weight='weight')

# Generate a figure of the city using Plotly
fig = go.Figure()

# Create a grid layout for nodes for a more realistic city view
num_nodes = len(G.nodes)
grid_size = int(num_nodes**0.5) + 1
x_coords = list(range(grid_size))
y_coords = list(range(grid_size))
pos = {}

for i, node in enumerate(G.nodes()):
    pos[node] = (x_coords[i % grid_size], y_coords[i // grid_size])

# Define symbols for different types of nodes
node_symbols = {'house': 'circle', 'mall': 'square', 'petrol': 'triangle-up'}

# Add nodes to the figure with symbols
for node in G.nodes():
    x, y = pos[node]
    if 'house' in node:
        color = 'blue'
        symbol = node_symbols['house']
    elif 'mall' in node:
        color = 'red'
        symbol = node_symbols['mall']
    elif 'petrol' in node:
        color = 'green'
        symbol = node_symbols['petrol']
    fig.add_trace(go.Scatter(x=[x], y=[y], mode='markers', marker=dict(size=15, color=color, symbol=symbol), text=node, name=node))

# Add edges to the figure
for edge in G.edges(data=True):
    source, target, weight = edge
    x0, y0 = pos[source]
    x1, y1 = pos[target]
    if (source, target) in zip(shortest_path, shortest_path[1:]):
        color = 'darkred'
        width = 3
    else:
        color = 'grey'
        width = 1
    fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines', line=dict(width=width, color=color), name=f"{source} - {target} ({weight['weight']})"))

# Highlight the shortest path in the figure and add distance annotations
annotations = []
for i in range(len(shortest_path)-1):
    source, target = shortest_path[i], shortest_path[i+1]
    x0, y0 = pos[source]
    x1, y1 = pos[target]
    fig.add_trace(go.Scatter(x=[x0, x1], y=[y0, y1], mode='lines', line=dict(width=3, color='orange'), name='shortest path'))
    # Add distance annotations
    mid_x, mid_y = (x0 + x1) / 2, (y0 + y1) / 2
    distance = G[source][target]['weight']
    annotations.append(dict(x=mid_x, y=mid_y, text=f"{distance} km", showarrow=False, font=dict(color='black', size=12)))

# Determine the symbol for the starting and ending locations
def get_node_type(node):
    if 'house' in node:
        return 'house'
    elif 'mall' in node:
        return 'mall'
    elif 'petrol' in node:
        return 'petrol'

# Add markers for the starting and ending locations
fig.add_trace(go.Scatter(x=[pos[source][0]], y=[pos[source][1]], mode='markers+text', marker=dict(size=20, color='black', symbol=node_symbols[get_node_type(source)]), text=[source], textposition='top center', name=source))
fig.add_trace(go.Scatter(x=[pos[target][0]], y=[pos[target][1]], mode='markers+text', marker=dict(size=20, color='black', symbol=node_symbols[get_node_type(target)]), text=[target], textposition='top center', name=target))

# Add a title and axis labels
fig.update_layout(title='City Map', xaxis=dict(title='X Axis', showgrid=False), yaxis=dict(title='Y Axis', showgrid=False), showlegend=True, annotations=annotations)

# Add legend for the node types and colors
fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=15, color='blue', symbol=node_symbols['house']), legendgroup='house', showlegend=True, name='House'))
fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=15, color='red', symbol=node_symbols['mall']), legendgroup='mall', showlegend=True, name='Mall'))
fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers', marker=dict(size=15, color='green', symbol=node_symbols['petrol']), legendgroup='petrol', showlegend=True, name='Petrol Station'))
fig.add_trace(go.Scatter(x=[None], y=[None], mode='lines', line=dict(width=3, color='orange'), legendgroup='path', showlegend=True, name='Shortest Path'))

# Show the figure
fig.show()

# Print the shortest path and its total distance
print(f"The shortest path from {source} to {target} is:")
for i in range(len(shortest_path)-1):
    print(f"{shortest_path[i]} -> ", end='')
print(f"{shortest_path[-1]}")
total_distance = sum([G[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1)])
print(f"The total distance is: {total_distance} km")
