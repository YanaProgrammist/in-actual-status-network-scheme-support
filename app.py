from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd


from components.network_scheme import NetworkScheme

from callbacks.network_scheme_callbacks import handle_drag_and_drop

# test
# Создаем экземпляр графа
network = NetworkScheme("213")

# Добавляем узлы
network.add_node('router1', 100, 100, 'Router-1', 'network_device', 40)
network.add_node('switch1', 300, 100, 'Switch-1', 'network_device', 35)
network.add_node('pc1', 200, 300, 'PC-User1', 'PC', 30)
network.add_node('server1', 400, 200, 'Server-1', 'network_device', 45)

# Добавляем связи
network.add_link('router1', 'switch1', 'blue', 3)
network.add_link('switch1', 'pc1', 'green', 2)
network.add_link('switch1', 'server1', 'red', 2)
network.add_link('pc1', 'server1', 'orange', 1)

app = Dash()

app.layout = html.Div(children=[
    html.H1(children='Актуальное состояние схем сети'),
    html.Div([
        html.Button("Добавить сетевое устройство", id="add-network-device-btn"),
        html.Button("Добавить компьютер", id="add-pc-btn"),
        html.Button("Очистить схему", id="clear-btn"),
    ], style={'margin': '10px'}),
    dcc.Graph(
        id='network-scheme',
        figure=network.create_scheme(),
        config={
            'modeBarButtonsToAdd': ['drawrect', 'drawcircle', 'eraseshape'],
            'displayModeBar': True
        },
    ),
    html.Div(id='info'),
    dcc.Store(id='network-data', data={
        'nodes': network.nodes,
        'links': network.links
    })
])

if __name__ == '__main__':
    app.run(debug=True)
