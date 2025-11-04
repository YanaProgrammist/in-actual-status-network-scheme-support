from data.dto import DeviceDTO
from data.models import DeviceType, DeviceStatus

from dash import html, callback, Input, Output, State, dcc

add_device_modal_id = "create-modal"
create_button = html.Div([html.Button("Добавить устройство", id="add-device-btn", disabled=True, )])

inputs = html.Div([
    dcc.Dropdown(
        id='add-network-device-type',
        options=[
            {'label': device_type.value, 'value': device_type.name}
            for device_type in DeviceType
        ],
        value=DeviceType.PC.name,
        placeholder='Выберите тип устройства',
        style={'margin': '10px', 'width': '200px'}
    ),
    dcc.Input(
        id="add-network-device-name",
        placeholder='Введите название девайса',
        type='text',
        style={'margin': '10px', 'width': '90%', }
    ),
    dcc.Textarea(
        id="add-network-device-description",
        placeholder='Введите описание девайса',
        style={
            'width': '90%',
            'height': '350px',
            'margin': '10px',
            'resize': 'vertical',
            'whiteSpace': 'pre-wrap',
            'wordWrap': 'break-word',
            'overflowY': 'auto'
        }
    )
], style={'display': 'flex', 'flexDirection': 'column'})


def add_test_data():
    devices = [DeviceDTO(type=DeviceType.PC, name="Test device 1", description="test descr",
                         status=DeviceStatus.ACTIVE),
               DeviceDTO(type=DeviceType.NETWORK_DEVICE, name="Test device 2", description="test descr 2",
                         status=DeviceStatus.ACTIVE)
               ]
    res = []
    for device in devices:
        shape = 'square' if device.type == DeviceType.NETWORK_DEVICE else 'circle'
        hover = "<br>".join([f"{k}: {v}" for k, v in device.model_dump().items()])
        res.append({'data':
            {
                'id': device.id,
                'label': device.name,
                'shape': shape,
                'tooltip': f"{hover}<extra></extra>",
                'model': device.model_dump_json(),
            },
        })
    return res


@callback(
    Output('network-scheme', 'elements'),
    Output('add-network-device-name', 'value'),
    Output('add-network-device-description', 'value'),
    Input('add-device-btn', 'n_clicks'),
    State('network-scheme', 'elements'),
    State('add-network-device-type', 'value'),
    State('add-network-device-name', 'value'),
    State('add-network-device-description', 'value'),
    prevent_initial_call=True
)
def add_device_buttons_callback(add_button, elements, device_type_value, device_name, device_description):
    device_type = DeviceType[device_type_value] if device_type_value else DeviceType.PC
    new_device = DeviceDTO(type=device_type, name=device_name, description=device_description,
                           status=DeviceStatus.ACTIVE)
    hover = "<br>".join([f"{k}: {v}" for k, v in new_device.model_dump().items()])
    shape = 'square' if new_device.type == DeviceType.NETWORK_DEVICE else 'circle'
    elements.append(
        {'data':
            {
                'id': new_device.id,
                'label': new_device.name,
                'shape': shape,
                'tooltip': f"{hover}<extra></extra>",
                'model': new_device.model_dump_json(),
            },
        })
    return elements, '', ''


@callback(
    Output('add-device-btn', 'disabled'),
    Output('add-network-device-name', 'style'),
    Output('add-network-device-description', 'style'),
    Input('add-network-device-name', 'value'),
    Input('add-network-device-description', 'value')
)
def validate_inputs(name, description):
    base_style = {'margin': '10px', 'width': '90%'}
    error_style = {**base_style, 'border': '2px solid red'}

    name_valid = bool(name and name.strip())
    desc_valid = bool(description and description.strip())

    name_style = error_style if not name_valid else base_style
    desc_style = error_style if not desc_valid else base_style

    return not (name_valid and desc_valid), name_style, desc_style
