import plotly.graph_objects as go


class NetworkScheme:
    def __init__(self, location):
        self.location = location
        self.nodes = []
        self.links = []

    def add_node(self, node_id, x, y, name, node_type, size=30):
        self.nodes.append(
            {
                'id': node_id,
                'x': x, 'y': y,
                'name': name,
                'type': node_type,
                'size': size,
            }
        )

    def add_link(self, node_a, node_b, color='gray', width=2):
        self.links.append({
            'source': node_a,
            'target': node_b,
            'color': color,
            'width': width
        })

    def create_scheme(self):
        scheme = go.Figure()

        for link in self.links:
            source = next(node for node in self.nodes if node['id'] == link['source'])
            target = next(node for node in self.nodes if node['id'] == link['target'])

            scheme.add_trace(
                go.Scatter(
                    x=[source['x'], target['x'], None],
                    y=[source['y'], target['y'], None],
                    mode='lines',
                    line=dict(color=link['color'], width=link['width']),
                    hoverinfo='none',
                    showlegend=False
                )
            )

        for node in self.nodes:
            if node['type'] == 'PC':
                scheme.add_shape(
                    type="rect",
                    x0=node['x'] - node['size'] / 2, y0=node['y'] - node['size'] / 2,
                    x1=node['x'] + node['size'] / 2, y1=node['y'] + node['size'] / 2,
                    fillcolor='green',
                    opacity=0.7
                )
            elif node['type'] == 'network_device':
                scheme.add_shape(
                    type="rect",
                    x0=node['x'] - node['size'] / 2, y0=node['y'] - node['size'] / 3,
                    x1=node['x'] + node['size'] / 2, y1=node['y'] + node['size'] / 3,
                    fillcolor='blue',
                    opacity=0.7
                )

            scheme.add_trace(go.Scatter(
                x=[node['x']],
                y=[node['y']],
                mode='text',
                text=[node['name']],
                textposition="middle center",
                textfont=dict(size=10, color='black'),
                customdata=[node['id']],
                showlegend=False,
                hoverinfo='text',
                hovertext=f"{node['name']}<br>Тип: {node['type']}"
            ))

        scheme.update_layout(
            title=f"Схема сети {self.location}",
            xaxis=dict(range=[0, 600], constrain='domain', showgrid=True),
            yaxis=dict(range=[0, 500], scaleanchor='x', showgrid=True),
            width=900,
            height=600,
            plot_bgcolor='white',
            dragmode='drawrect',
            shapes=[]
        )

        return scheme
