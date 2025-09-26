import networkx as nx
import pandas as pa
import plotly.graph_objects as go

T = pa.read_csv('bus_metz_lignes.csv')

G = nx.from_pandas_edgelist(T, source='station_name1', target='station_name2', edge_attr='distance')

# Lecture des données
M = pa.read_csv('bus_metz_backup.csv')
print(M)
fig = go.Figure()

# Tracé du graphe
fig.add_trace(
    go.Scattergeo(
        mode='markers + text',
        lon=M['lon'],
        lat=M['lat'],
        text=M['display_name'].apply(lambda x: \
                                         '<b>' + str(x) \
                                         + '</b>'),
        textposition='middle center',
        textfont=dict(color="black", size=8, family='bold'),
        showlegend=False,
        marker={'symbol': 'circle-dot',
                'size': 30,
                'opacity': 0.8,
                'color': 'gray'}
    )
)
fig.update_layout(
    showlegend=True,
    legend={'x': 0,
            'y': 0.1,
            'title': '<b>Lignes : </b>',
            'orientation': 'h',
            'bordercolor': 'gray',
            'font': {'family': 'Verdana', 'size': 14},
            'borderwidth': 2,
            },
    title={'text': "<b>Lignes de Bus Ã  Metz</b>",
           'font': {'family': 'Verdana'},
           'y': 0.93,
           'x': 0.5}
)
fig.update_geos(
    fitbounds='locations',
    showland=True,
    landcolor='white',
    projection_type='natural earth'
)

N = M.groupby('name').first()
#print(N.head())

T['x1'] = [N.loc[n, 'lon'] for n in T['station_name1']]
T['y1'] = [N.loc[n, 'lat'] for n in T['station_name1']]
T['x2'] = [N.loc[n, 'lon'] for n in T['station_name2']]
T['y2'] = [N.loc[n, 'lat'] for n in T['station_name2']]
#print(T.head())

couleurs = ['black', 'green', 'blue', 'red', 'chocolate']
dot = ['dot', 'solid']
L= []
ListeLigne = ["A","B","1","2","3","4","4a","4b","5","5e","5f"]
compteur=0
for i in ListeLigne:
    A = T.query('line == @i')
    for k in A.index:
        fig.add_trace(
            go.Scattergeo(
                mode = 'lines',
                lon = [A.loc[k, 'x1'], A.loc[k, 'x2']],
                lat = [A.loc[k, 'y1'], A.loc[k, 'y2']],
                hovertext = A['distance'],
                opacity= 0.5,
                showlegend= True if i not in L else False,
                name = i,
                line = {'color' : couleurs[compteur%5 - 1],
                        'dash' : dot[compteur%2],
                        'width' : 4}
                        )
            )
        L.append(i)
    compteur+=1
fig.show()
