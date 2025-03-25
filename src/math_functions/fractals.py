# src/math_functions/fractals.py
import numpy as np

def generate_fractal(width, height, x_min, x_max, y_min, y_max, max_iter, polynomial):
    print(f"Generating fractal with width: {width}, height: {height}")  # Debugging
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    Z = np.zeros_like(C, dtype=complex)
    divergence_time = np.zeros(Z.shape, dtype=int)

    for i in range(max_iter):
        Z = polynomial.evaluate(Z, C)
        divergence_time[abs(Z) > 2] = i
        Z[abs(Z) > 2] = np.nan  # Stop iterating when divergent
    
    print(f"Shape of divergence_time: {divergence_time.shape}")  # Debugging
    print(f"Max value in divergence_time: {np.nanmax(divergence_time)}")  # Debugging
    print(f"Min value in divergence_time: {np.nanmin(divergence_time)}")  # Debugging

    return divergence_time
