from dash import Dash
import dash_bootstrap_components as dbc

from layout.main_layout import serve_main_layout

if __name__ == '__main__':
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = serve_main_layout
    app.run(debug=True,dev_tools_ui=False)
