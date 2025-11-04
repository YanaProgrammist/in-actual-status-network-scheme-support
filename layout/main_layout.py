from dash import html, dcc, callback, Output, Input, State
from dash_cytoscape import Cytoscape

from components.modal_window import ModalWindow
from data.dto import DeviceDTO
from layout.add_device_layout import inputs, create_button, add_device_modal_id, add_test_data
from layout.delete_device_layout import delete_button, body

create_modal = ModalWindow(add_device_modal_id, "Создать девайс", inputs, create_button)
delete_modal = ModalWindow("delete-device-modal", "Удалить девайс",body,delete_button)

stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'width': "30px",
            'height': "30px",
            'shape': 'data(shape)',
            'background-color': '#0074D9',
            'font-size': '12px'
        }
    },
    {
        'selector': 'node[shape="square"]',
        'style': {
            'background-color': '#FF851B'
        }
    },
]

main_layout = html.Div([
    html.H1(children='Актуальное состояние схем сети'),
    html.Div([
        create_modal.get_layout(),
        delete_modal.get_layout(),
    ], style={'margin': '10px', 'display': 'flex'}),

    html.Div([
        html.Div([
            Cytoscape(
                id='network-scheme',
                layout={'name': 'grid'},
                stylesheet=stylesheet,
                style={'width': '100%', 'height': '600px'},
                elements=add_test_data()
            )
        ], style={'display': 'inline-block', 'width': '70%'}),

        html.Div([
            html.H4("Информация об устройстве"),
            html.Div(id='hover-info')
        ], style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'padding': '20px'})
    ]),

    dcc.Store(id='selected-node', data=None)
])


@callback(
    Output('hover-info', 'children'),
    Input('network-scheme', 'mouseoverNodeData')
)
def display_hover_info(hover_data):
    if hover_data:
        device_data = DeviceDTO.model_validate_json(hover_data["model"])
        return html.Div([
            html.H5("Выбранное устройство:"),
            html.P(f"Название: {device_data.name}"),
            html.P(f"Тип: {device_data.type.name}"),
            html.P(f"Статус: {device_data.status.name}"),
            html.P(f"Описание: {device_data.description}")
        ])

    return html.P("Наведите на устройство для информации")


# @callback(
#     Output('selected-node', 'data'),
#     Output('delete-device-btn', 'style'),
#     Input('network-scheme', 'tapNode'),
#     State('selected-node', 'data'),
#     prevent_initial_call=True
# )
# def select_node(tap_node, current_selected):
#     pass
#     # if trigger_id == 'network-scheme' and tap_node:
#     #     # Клик на ноду
#     #     return tap_node['data']['id'], {'display': 'block', 'margin': '10px'}
#     # else:
#     #     # Клик на фон или другой элемент
#     #     return None, {'display': 'none'}


create_modal.get_callback()
delete_modal.get_callback()
