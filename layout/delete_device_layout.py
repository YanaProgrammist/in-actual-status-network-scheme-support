from dash import html, dcc, callback, Output, Input, State

from data.dto import DeviceDTO

delete_button = html.Div([html.Button("Удалить устройство", id="delete-device-btn", disabled=True, )])

body = html.Div([
    dcc.Dropdown(
        id='delete-device-dropdown',
        placeholder='Выберите устройство'
    ),
    html.Div(id='selected-device-info', style={'marginTop': '10px'})
], style={'display': 'flex', 'flexDirection': 'column'})


@callback(
    Output('delete-device-dropdown', 'options'),
    Input('network-scheme', 'elements')
)
def update_dropdown(elements):
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
    return options


@callback(
    Output('selected-device-info', 'children'),
    Output('delete-device-btn', 'disabled'),
    Input('delete-device-dropdown', 'value'),
    State('network-scheme', 'elements')
)
def display_selected_device(selected_id, elements):
    if selected_id:
        selected_device = next((elem for elem in elements if elem['data']['id'] == selected_id), None)
        if selected_device:
            device_data = DeviceDTO.model_validate_json(selected_device['data']['model'])
            info = html.Div([
                html.H5("Выбранное устройство:"),
                html.P(f"ID: {device_data.id}"),
                html.P(f"Название: {device_data.name}"),
                html.P(f"Тип: {device_data.type.name}"),
                html.P(f"Статус: {device_data.status.name}"),
                html.P(f"Описание: {device_data.description}")
            ])
            return info, False

    return "Устройство не выбрано", True


@callback(
    Output('network-scheme', 'elements', allow_duplicate=True),
    Input('delete-device-btn', 'n_clicks'),
    State('delete-device-dropdown', 'value'),
    State('network-scheme', 'elements'),
    prevent_initial_call=True
)
def delete_device(n_clicks, selected_id, elements):
    if n_clicks and selected_id:
        elements = [elem for elem in elements if elem['data']['id'] != selected_id]
    return elements
