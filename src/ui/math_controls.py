# math_controls.py
import dash_bootstrap_components as dbc
from dash import dcc, html

def create_polynomial_slider(degree, width='100%'):
    """
    Creates a slider and enable/disable checkbox for a polynomial coefficient.

    Args:
        degree (int): The degree of the polynomial coefficient.
        width (str): The width of the slider as a percentage.

    Returns:
        dbc.Col: A column containing the slider and checkbox.
    """
    slider = dbc.Col([
        dbc.Label(f"Coefficient x^{degree}", style={'fontSize': '0.9rem', 'color': '#ddd', 'textShadow': '1px 1px 2px black'}),
        dcc.Slider(
            id=f"polynomial-coeff-{degree}",
            min=-5,
            max=5,
            step=0.1,
            value=0,
            className='slider',  # Add a class for styling
            persistence=True,  # Enable persistence
            persistence_type='memory',  # Store in memory (other options: 'local', 'session')
            marks=None  # Remove slider marks
        ),
        dbc.Checklist(
            options=[{"label": "Enable", "value": "enabled"}],
            value=["enabled"],
            id=f"polynomial-coeff-enable-{degree}",
            switch=True,
            labelStyle={'fontSize': '0.8rem', 'color': '#ccc', 'textShadow': '1px 1px 2px black'}
        ),
    ], width=width)  # Setting the width of the column

    return slider
