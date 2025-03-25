# app.py
import io
import base64
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from math_functions.polynomials import Polynomial, generate_polynomial_image

print("Polynomial class imported successfully!")

# Constants
CALCULATION_WIDTH = 800
CALCULATION_HEIGHT = 800
x_min = -2
x_max = 2
y_min = -2
y_max = 2

# --- Initial Polynomial Degrees ---
initial_degrees = [0]  # Only Y-int is initially enabled
max_degree = 2  # Set max degree to 2
degrees = list(range(max_degree + 1))

# --- App Layout ---
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

# --- UI Generation Functions ---
def generate_polynomial_sliders(degrees):
    sliders = []
    for degree in degrees:
        if degree == 0:
            label = "Y-int/Height"
        elif degree == 1:
            label = "1st Degree"
        elif degree == 2:
            label = "2nd Degree"
        elif degree == 3:
            label = "3rd Degree"
        else:
            label = f"{degree}th Degree"  # For degrees > 3
        slider = dbc.Card(
            dbc.CardBody([
                dbc.Label(label, html_for=f"polynomial-coeff-{degree}"),
                dbc.Row([
                    dbc.Col([
                        dbc.Checklist(
                            options=[{"label": "", "value": "enabled"}],
                            value=["enabled"] if degree == 0 else [],  # Only enable Y-int initially
                            id=f"polynomial-coeff-enable-{degree}",
                            switch=True,
                            style={'verticalAlign': 'middle'}
                        ),
                    ], width=2, style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
                    dbc.Col([
                        dcc.Slider(
                            id=f"polynomial-coeff-{degree}",
                            min=-5,
                            max=5,
                            step=0.1,
                            value=0,
                            className='slider',
                            persistence=True,
                            persistence_type='memory',
                            marks=None
                        ),
                    ], width=10),
                ], align="center"),
            ]),
            className="mb-3",
        )
        sliders.append(slider)
    return sliders

# --- App Layout ---
app.layout = dbc.Container([
    html.H1("Polynomial Painter"),
    dbc.Row([
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Functions"),
                    html.H5("Polynomial"),  # Added Polynomial title
                    html.Div(id='polynomial-sliders-container', children=generate_polynomial_sliders(degrees)),
                    html.H6("Colors"),
                    dbc.Label("Color Above Line", html_for="color-above"),
                    dcc.Input(
                        id="color-above",
                        type="color",
                        value="#FFFF00"  # Initial yellow color
                    ),
                    dbc.Label("Color Below Line", html_for="color-below"),
                    dcc.Input(
                        id="color-below",
                        type="color",
                        value="#800080"  # Initial purple color
                    ),
                ]),
                className="mb-3",
            ),
        ], md=4),
        dbc.Col([
            html.Img(id='polynomial-image', src="data:image/png;base64,", style={'width': '800px', 'height': '800px'}),
            dbc.Card(
                dbc.CardBody([
                    html.H4("Output"),
                    html.H5("Polynomial Function"),  # Title for the Output section
                    html.Div(id='polynomial-expression', children="f(x) = 0", style={'fontFamily': 'monospace', 'fontSize': '14px'}),
                ]),
                className="mt-3",
                style={'fontFamily': 'monospace', 'fontSize': '14px'}
            ),
        ], md=8),
    ]),
], fluid=True)

# --- Callbacks ---
all_inputs = [Input(f"polynomial-coeff-{degree}", 'value') for degree in degrees] + \
             [Input(f"polynomial-coeff-enable-{degree}", 'value') for degree in degrees] + \
             [Input("color-above", 'value'), Input("color-below", 'value')]

@app.callback(
    Output('polynomial-image', 'src'),
    Output('polynomial-expression', 'children'),
    all_inputs
)
def update_polynomial_image(*args):
    num_degrees = len(degrees)
    coefficients = args[:num_degrees]
    enabled_states = args[num_degrees:]
    color_above = args[-2]
    color_below = args[-1]

    coeff_dict = {degree: coeff if enabled else 0 for degree, coeff, enabled in zip(degrees, coefficients, enabled_states)}

    polynomial = Polynomial(coeff_dict)
    image_data = generate_polynomial_image(CALCULATION_WIDTH, CALCULATION_HEIGHT, x_min, x_max, y_min, y_max, polynomial, color_above, color_below)

    img = Image.fromarray(image_data)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    image_bytes = buf.getvalue()
    image_base64 = base64.b64encode(image_bytes).decode("ascii")

    # Update polynomial expression
    terms = []
    for degree, coeff, enabled in zip(degrees, coefficients, enabled_states):
        if enabled and coeff != 0:
            if degree == 0:
                term = f"{coeff:.2f}"
            elif degree == 1:
                term = f"{coeff:.2f}x"
            else:
                term = f"{coeff:.2f}x<sup>{degree}</sup>"

            terms.append(term)

    if not terms:
        expression = "f(x) = 0"
    else:
        expression = "f(x) = " + " + ".join(terms)

    return f"data:image/png;base64,{image_base64}", html.Div(dcc.Markdown(expression), style={'fontFamily': 'monospace', 'fontSize': '14px'})

if __name__ == '__main__':
    app.run_server(debug=True)
