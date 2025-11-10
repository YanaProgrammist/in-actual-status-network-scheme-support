from dash import html, dcc, callback, Output, Input, State
from dash_cytoscape import Cytoscape

from components.device_information import DeviceInformation
from components.modal_window import ModalWindow
from data.device_repo import get_all_devices
from layout.add_device_layout import inputs, create_button, add_device_modal_id
from layout.delete_device_layout import delete_button, body

create_modal = ModalWindow(add_device_modal_id, "Создать девайс", inputs, create_button)
delete_modal = ModalWindow("delete-device-modal", "Удалить девайс", body, delete_button)
device_information = DeviceInformation()

stylesheet = [
    {
        'selector': 'node',
        'style': {
            'content': 'data(label)',
            'width': "30px",
            'height': "30px",
            'shape': 'data(shape)',
            'background-opacity': 0,
            'background-fit': 'contain',
            'background-clip': 'none',
            'font-size': '12px'
        }
    },
    {'selector': 'edge', 'style': {'line-color': 'black', 'width': 2}},
    {
        'selector': '.selected',
        'style': {
            'border-width': '3px',
            'border-color': 'red',
            'border-opacity': 1
        }
    },
    {
        'selector': 'node[type="PC"]',
        'style': {
            'background-image': '/assets/images/pc.png'
        }
    },
    {
        'selector': 'node[type="NETWORK_DEVICE"]',
        'style': {
            'background-image': '/assets/images/network_device.png'
        }
    }
]


def get_init_devices():
    all_devices = get_all_devices()
    res = []
    for device in all_devices:
        res.append({'data':
            {
                'id': device.id,
                'label': device.name,
                'type': device.type.name,
                'model': device.model_dump_json(),
            },
        })
    return res


def serve_main_layout():
    return html.Div([
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
                    style={'width': '100%', 'height': '600px', 'backgroundColor': 'white', 'margin': '10px'},
                    elements=get_init_devices()
                )
            ], style={'display': 'inline-block', 'width': '70%'}),

            device_information.get_layout()
        ]),

        dcc.Store(id='selected-node', data=[]),
    ])


create_modal.get_callback()
delete_modal.get_callback()
device_information.get_callback()


@callback(
    Output('network-scheme', 'elements', allow_duplicate=True),
    Input('selected-node', 'data'),
    State('network-scheme', 'elements'),
    prevent_initial_call=True
)
def update_selected(selected_node_data, current_elements):
    if len(selected_node_data) == 0:
        element = next((el for el in current_elements if el.get('classes') == 'selected'), None)
        if element:
            element['classes'] = ''
    else:
        element = next((el for el in current_elements if el['data']['id'] == selected_node_data[0]), None)
        if element:
            element['classes'] = 'selected'
    return current_elements


@callback(
    Output('selected-node', 'data', allow_duplicate=True),
    Output('network-scheme', 'elements', allow_duplicate=True),
    Input('network-scheme', 'tapNode'),
    State('network-scheme', 'elements'),
    State('selected-node', 'data'),
    prevent_initial_call=True
)
def connect_devices_and_unselect(tap_node, current_elements, selected_node_data):
    if len(selected_node_data) == 0:
        selected_node_data.append(tap_node['data']['id'])
    else:
        element_a = next((el for el in current_elements if el['data']['id'] == selected_node_data[0]), None)
        element_b = next((el for el in current_elements if el['data']['id'] == tap_node['data']['id']), None)
        connect_devices(element_a, element_b, current_elements)
        selected_node_data = []
    return selected_node_data, current_elements


def connect_devices(device_a, device_b, elements):
    if not device_a or not device_b or device_a == device_b:
        return elements

    # создаём уникальный id для ребра
    edge_id = f"{device_a['data']['id']}_{device_b['data']['id']}"

    # проверяем, что такого ребра ещё нет
    if any(el.get('data', {}).get('id') == edge_id for el in elements):
        return elements

    # добавляем ребро
    new_edge = {
        'data': {
            'id': edge_id,
            'source': device_a['data']['id'],
            'target': device_b['data']['id']
        }
    }
    elements.append(new_edge)
    return elements
