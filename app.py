from dash import Dash
import dash_bootstrap_components as dbc

from layout.main_layout import main_layout

if __name__ == '__main__':
    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = main_layout
    app.run(debug=True)
