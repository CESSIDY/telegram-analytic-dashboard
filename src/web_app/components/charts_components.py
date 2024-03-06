from dash import html, dcc

from . import generate_section_banner


class ChartsComponents:
    def build_top_panel(self):
        return html.Div(
            id="top-section-container",
            className="row",
            children=[
                # Metrics summary
                html.Div(
                    id="metric-summary",
                    className="eight columns",
                    children=[
                        generate_section_banner("Metrics Summary"),
                        html.Div(
                            id="metric-div",
                            children=[],  # TODO Add some metrics
                        ),
                    ],
                ),
                # Piechart
                html.Div(
                    id="piechart-outer",
                    className="four columns",
                    children=[
                        generate_section_banner("% Some data"),
                        self.generate_piechart(),  # TODO Fill pie chart
                    ],
                ),
            ],
        )

    def generate_piechart(self):
        return dcc.Graph(
            id="piechart",
            figure={
                "data": [
                    {
                        "labels": [],
                        "values": [],
                        "type": "pie",
                        "marker": {"line": {"color": "white", "width": 1}},
                        "hoverinfo": "label",
                        "textinfo": "label",
                    }
                ],
                "layout": {
                    "margin": dict(l=20, r=20, t=20, b=20),
                    "showlegend": True,
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                    "font": {"color": "white"},
                    "autosize": True,
                },
            },
        )
