from dash import dash_table, html, dcc


def generate_section_banner(title):
    return html.Div(className="section-banner", children=title)
