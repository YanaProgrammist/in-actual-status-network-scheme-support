from dash import html, Output, Input, State, callback, dcc

from components.modal_window import ModalWindow
from data.device_repo import update_device
from data.dto import DeviceDTO
import dash_bootstrap_components as dbc

from data.models import DeviceStatus, DeviceType, Device


class DeviceInformation:
    def __init__(self):
        update_button = html.Div([
            html.Button("Обновить устройство", id="update_modal_btn", disabled=True)
        ])
        body = html.Div([
            dcc.Dropdown(
                id='update-device-dropdown',
                placeholder='Выберите устройство'
            ),
            html.Div(id='update-device-info', style={'marginTop': '10px'})
        ], style={'display': 'flex', 'flexDirection': 'column'})
        self.update_modal = ModalWindow("update_device_modal", "Обновить информацию", body, update_button)

    def get_layout(self):
        return html.Div(
            [
                html.H4("Информация об устройстве"),
                html.Div(html.P("Выберите устройство для информации"), id='hover-info', )
            ], style={'display': 'inline-block', 'width': '30%', 'verticalAlign': 'top', 'padding': '20px'}
        )

    def get_callback(self):
        self.update_modal.get_callback()
        self.update_modal.external_modal_close("update_modal_btn")


        @callback(
            Output('hover-info', 'children'),
            State('network-scheme', 'tapNode'),
            Input('selected-node', 'data'),
            prevent_initial_call=True
        )
        def show_info(tap_node, current_node):
            if len(current_node) == 0:
                info_div = html.P("Выберите устройство для информации")
            else:
                device_data = DeviceDTO.model_validate_json(tap_node['data']['model'])
                info_div = html.Div([
                    html.H5("Выбранное устройство:"),
                    html.P(f"Название: {device_data.name}"),
                    html.P(f"Тип: {device_data.type.name}"),
                    html.P(f"Статус: {device_data.status.name}"),
                    html.P(f"Описание: {device_data.description}"),
                    self.update_modal.get_layout(),
                ])

            return info_div

        @callback(

            Output('update-device-dropdown', 'options'),
            Output('update-device-dropdown', 'value'),
            Input('network-scheme', 'elements'),
            State('selected-node', 'data')
        )
        def update_dropdown(elements, selected):
            options = [
                {
                    'label': html.Div([
                        html.Div(f"Name: {elem['data'].get('label', 'Unnamed')}", style={'fontWeight': 'bold'}),
                        html.Div(f"ID: {elem['data']['id']}", style={'fontSize': '12px', 'color': 'gray'})
                    ]),
                    'value': elem['data']['id']
                }
                for elem in elements
            ]
            return options, selected[0] if not [] else None

        @callback(
            Output('update-device-info', 'children'),
            Output('update_modal_btn', 'disabled'),
            Input('update-device-dropdown', 'value'),
            State('network-scheme', 'elements'),
            Input('selected-node', 'data')
        )
        def display_selected_device(selected_id, elements, test):
            if selected_id:
                selected_device = next((elem for elem in elements if elem['data']['id'] == selected_id), None)
                if selected_device:
                    device_data = DeviceDTO.model_validate_json(selected_device['data']['model'])
                    info = html.Div([
                        html.H5("Выбранное устройство:"),
                        html.P(f"ID: {device_data.id}"),
                        dcc.Dropdown(
                            id='update-device-type',
                            placeholder='Тип устройство',
                            options=[{"label": s.value, "value": s.value} for s in DeviceType],
                            value=device_data.type.value,
                            clearable=False
                        ),
                        dcc.Dropdown(
                            id='update-device-status',
                            options=[{"label": s.value, "value": s.value} for s in DeviceStatus],
                            value=device_data.status.value,
                            placeholder='Статус устройство',
                            clearable=False
                        ),
                        dcc.Input(
                            id="update-network-device-name",
                            placeholder='Введите название девайса',
                            value=device_data.name,
                            type='text',
                            style={'margin': '10px', 'width': '90%', }
                        ),
                        dcc.Textarea(
                            id="update-network-device-description",
                            placeholder='Введите описание девайса',
                            value=device_data.description,
                            style={
                                'width': '90%',
                                'height': '350px',
                                'margin': '10px',
                                'resize': 'vertical',
                                'whiteSpace': 'pre-wrap',
                                'wordWrap': 'break-word',
                                'overflowY': 'auto'
                            }
                        ),

                    ])
                    return info, False

            return "Устройство не выбрано", True

        @callback(
            Output('network-scheme', 'elements', allow_duplicate=True),
            Output('selected-node', 'data', allow_duplicate=True),
            Input('update_modal_btn', 'n_clicks'),
            State('update-device-dropdown', 'value'),
            State('update-device-type', 'value'),
            State('update-device-status', 'value'),
            State('update-network-device-name', 'value'),
            State('update-network-device-description', 'value'),
            State('network-scheme', 'elements'),
            prevent_initial_call=True
        )
        def update_device_callback(n_clicks, device_id, type_, status_, name_, desc_, elements):
            if not n_clicks:
                return elements, []

            new_data = DeviceDTO(
                id=device_id,
                type=type_,
                status=status_,
                name=name_,
                description=desc_
            )
            update_device(new_data)
            for elem in elements:
                if elem['data']['id'] == device_id:
                    elem['data']['label'] = new_data.name
                    elem['data']['type'] = new_data.type.name
                    elem['data']['model'] = new_data.model_dump_json()

            return elements , []
