# pip install plotly
# python -m pip install plotly

# benutzt JavaScript
# erstellt komplette, eigentständige HTML

# Graph als Objekt
import plotly.io as pio
import plotly.graph_objects as go

graph = go.Figure(
    data=go.Bar(
        x=["a", "b", "c"],
        y=[42, 23, 697]
    ),
    layout=go.Layout(
        title=go.layout.Title(text="Netter Plot")
    )
)

# normalerweise im Browser angezeigt
graph.show(renderer='browser')

# einfacher für Vorstellung
graph.show()


# als HTML speichern
# einfach einzubetten und zu weiterzugeben
graph.write_html('assets/netter_plot.html', auto_open=True)

# Graph aus Dictionary
import plotly.io as pio

fig = dict({
    "data": [
        {
            "type": "bar",
            "x": ["a", "b", "c"],
            "y": [42, 23, 697]
        }
    ],
    "layout": {
        "title": {
            "text": "Netter Plot"
        }
    }
})

pio.show(fig)


# weitere Abstaktionsebene: Plotly Express
import plotly.express as px

fig = px.bar(
    x=["a", "b", "c"],
    y=[42, 23, 697]
)

fig.show()


# plotly kann verschiedene Grafikformate ins eigene Format überführen:
# matplotlib, ggplot2, etc.

# pandas direkt mit plotly nutzen
import pandas as pd
df = pd.DataFrame(
    data=[42,23, 697],
    index=["a", "b", "c"]
)

df.plot.bar()

# plotting backend von matplotlib (default) zu plotly ändern
pd.options.plotting.backend = "plotly"

fig = df.plot.bar()
fig.show()

# aus plotly direkt auf Gapminder zugreifen
germany = px.data.gapminder().query("country == 'Germany'")

fig = px.bar(
    germany,
    x="year",
    y="pop"
)

fig.show()


# Scatterplot aus gapminder
life_exp2015 = px.data.gapminder("year == 2015")
fig = px.scatter(
    life_exp2015,
    x="gdpPercap",
    y="lifeExp",
    color="continent"
    #, hover_name="country"
)

fig.show()

# Achsen logarithmisch darstellen
fig.update_layout(
    xaxis_type="log",
    yaxis_type="log"
)

fig.show()

### Scatter-Matrix
import plotly.express as px
df = px.data.iris()
fig = px.scatter_matrix(df)
fig.show()


### Zur Erzeugung von Netzwerkgraphen in plotly ist es notwendig, das
### Grundgerüst per NetworkX zu erstellen.
### Da plotly nicht weiß, wie es Punkte für Personen platzieren soll, lässt man
### diese durch NetworkX willkürlich vorgeben.
### Plotly legt dann zwei Scatterplots - einen für die Personen und einen für
### die Kanten zwischen diesen - übereinander

### networkx

import networkx as nx
import matplotlib.pyplot as plt

edgelist = "data/ger000088-lessing-emilia-galotti.csv"

df = pd.read_csv(edgelist)

### einen ungerichteten Graphen erstellen
G = nx.convert_matrix.from_pandas_edgelist(
    df,
    source="Source",
    target="Target",
    edge_attr="Weight"
)

### willkürliche Positionen festlegen
pos = nx.spring_layout(G)

for n, p in pos.items():
    G.nodes[n]['pos'] = p

### die Positionen den Punkten übergeben
G.add_nodes_from(pos.keys())

### eine Kantenliste erstellen, der man die Start- und Endkoordinaten der

edge_x = []
edge_y = []

### einzelnen Kanten übergibt
for edge in G.edges():
    x0, y0 = G.nodes[edge[0]]['pos']
    x1, y1 = G.nodes[edge[1]]['pos']
    edge_x.append(x0)
    edge_x.append(x1)
    edge_x.append(None)
    edge_y.append(y0)
    edge_y.append(y1)
    edge_y.append(None)


### Knotenliste mit Koordinaten
node_x = []
node_y = []
for node in G.nodes():
    x, y = G.nodes[node]['pos']
    node_x.append(x)
    node_y.append(y)

### Liste für Knotenlabel
node_text = []
for node in G.nodes():
    node_text.append('{}'.format(node))

#### ende NetworkX-Teil

### Scatterplot aus Kantenliste
edge_trace = go.Scatter(
    x=edge_x,
    y=edge_y,
    line=dict(width=0.5, color='#000'),
    hoverinfo="none",
    mode="lines"
)

### Scatterplot aus Knotenliste
node_trace = go.Scatter(
    x=node_x, y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='Jet',
        reversescale=True,
        color=[],
        size=10,
        colorbar=dict(
            thickness=15,
            xanchor='left',
            titleside='right'
        ),
        line_width=2))

### Labels den Knoten zuweisen
node_trace.text = node_text


### Grade der Knoten bestimmen
node_adjacencies = []
for node, adjacencies in enumerate(G.adjacency()):
    node_adjacencies.append(len(adjacencies[1]))
    node_text.append('# of connections: '+str(len(adjacencies[1])))

### den Knoten Farben nach Grad zuweisen
node_trace.marker.color = node_adjacencies


### plotly-Figure erstellen
fig = go.Figure(data=[edge_trace, node_trace],
             layout=go.Layout(
                title='Figuren in Emilia Galotti',
                titlefont_size=16,
                showlegend=False,
                hovermode='closest',
                margin=dict(b=20,l=5,r=5,t=40),
                annotations=[ dict(
                    showarrow=False,
                    xref="paper", yref="paper",
                    x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                )
                )

fig.show(renderer="browser")
