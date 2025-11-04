from dash import html,  Output, Input, State, callback
import dash_bootstrap_components as dbc


class ModalWindow:
    def __init__(self, modal_id, button_txt="открыть", body_elements=None, footer_elements=None):
        self.modal_id = modal_id
        self.button_txt = button_txt
        self.body_elements = body_elements
        self.footer_elements = footer_elements

    def get_layout(self):
        return html.Div(
            [
                dbc.Button(self.button_txt, id=f"{self.modal_id}_open", n_clicks=0),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle(self.button_txt)),
                        dbc.ModalBody(self.body_elements),
                        dbc.ModalFooter([
                            self.footer_elements,
                            dbc.Button("Закрыть", id=f"{self.modal_id}_close",
                                       className="ms-auto", n_clicks=0)
                        ]),
                    ],
                    id=self.modal_id,
                    is_open=False,
                ),
            ]
        )

    def get_callback(self):
        @callback(
            Output(self.modal_id, "is_open"),
            [Input(f"{self.modal_id}_open", "n_clicks"),
             Input(f"{self.modal_id}_close", "n_clicks")],
            [State(self.modal_id, "is_open")],
            prevent_initial_call=True
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open