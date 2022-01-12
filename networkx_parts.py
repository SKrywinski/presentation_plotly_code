### networkx

import networkx as nx
import matplotlib.pyplot as plt

edgelist = "ger000088-lessing-emilia-galotti.csv"

df = pd.read_csv(edgelist)

G = nx.convert_matrix.from_pandas_edgelist(
    df,
    source="Source",
    target="Target",
    edge_attr="Weight"
)

pos = nx.spring_layout(G)

for n, p in pos.items():
    G.nodes[n]['pos'] = p

G.add_nodes_from(pos.keys())

edge_x = []
edge_y = []

for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)


node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

node_text = []
for node in G.nodes():
    node_text.append('{}'.format(node))

####


edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color='#000'),
    hoverinfo="none",
    mode="lines"
)

node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode="markers",
    hoverinfo="text"
)


node_trace.text = node_text

fig = go.Figure(
    data=[edge_trace, node_trace],
    layout=go.Layout(
        title="Figuren in Emilia Galotti",
        showlegend=False,
        hovermode="closest",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
    )
)

fig.show()
