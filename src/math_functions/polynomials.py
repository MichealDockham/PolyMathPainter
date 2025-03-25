# src/math_functions/polynomials.py
import numpy as np
import matplotlib.pyplot as plt

class Polynomial:
    def __init__(self, coefficients):
        self.coefficients = coefficients

    def evaluate(self, x, y):
        # Only use the y-intercept (degree 0)
        return self.coefficients.get(0, 0)  # Return Y-int value

def generate_polynomial_image(width, height, x_min, x_max, y_min, y_max, polynomial, color_above, color_below):
    y_int = polynomial.evaluate(0, 0)  # Get the y-intercept value

    # Create a grid of y-values
    y = np.linspace(y_min, y_max, height)
    xv, yv = np.meshgrid(np.linspace(x_min, x_max, width), y)

    # Create an image where the color depends on the y-value relative to y_int
    image_data = np.zeros((height, width, 3))  # Initialize with black

    # Scale y_int to the range [0, height]
    y_int_scaled = int(((y_int - y_min) / (y_max - y_min)) * height)

    # Convert hex colors to RGB
    color_above_rgb = tuple(int(color_above[i:i+2], 16) / 255.0 for i in (1, 3, 5))
    color_below_rgb = tuple(int(color_below[i:i+2], 16) / 255.0 for i in (1, 3, 5))

    # Color the image based on the scaled y_int
    if 0 <= y_int_scaled <= height:  # Corrected the condition
        image_data[:y_int_scaled, :, :] = color_above_rgb  # Color above
        image_data[y_int_scaled:, :, :] = color_below_rgb  # Color below
    elif y_int_scaled < 0:
        image_data[:, :, :] = color_below_rgb # Color all with below color
    else:
        image_data[:, :, :] = color_above_rgb # Color all with above color

    image_data = (image_data * 255).astype(np.uint8)
    return image_data
