from dash import Dash, html, dcc, Input, Output, State, callback


@callback(
    Output('network-scheme', 'figure'),
    Output('network-data', 'data'),
    Output('info', 'children'),
    Input('network-scheme', 'relayoutData'),
    State('network-data', 'data'),
    prevent_initial_call=True
)
def handle_drag_and_drop(relayout_data, network_data):
    if not relayout_data:
        return dash.no_update, dash.no_update, "Нет данных о перемещении"

    if 'shapes' in relayout_data:
        updated_nodes = network_data['nodes'].copy()
        for i, shape in enumerate(relayout_data['shapes']):
            if i < len(updated_nodes):
                if 'x0' in shape and 'y0' in shape and 'x1' in shape and 'y1' in shape:
                    x_center = (shape['x0'] + shape['x1']) / 2
                    y_center = (shape['y0'] + shape['y1']) / 2
                    updated_nodes[i]['x'] = x_center
                    updated_nodes[i]['y'] = y_center
        figure.nodes = updated_nodes
        new_figure = figure.create_scheme()
        new_data = {'nodes': updated_nodes, 'links': network_data['links']}

        return new_figure, new_data, "Позиции устройств обновлены"

    return dash.no_update, dash.no_update, "Перетащите устройства для изменения схемы"

