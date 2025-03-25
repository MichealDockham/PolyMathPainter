# test_polynomials.py
from src.math_functions.polynomials import Polynomial

# Create two polynomials
p1 = Polynomial([1, 2, 3])  # 1 + 2x + 3x^2
p2 = Polynomial([4, 5])     # 4 + 5x

# Print the polynomials
print("Polynomial 1:", p1)
print("Polynomial 2:", p2)

# Evaluate the polynomials at x = 2
print("Polynomial 1 at x=2:", p1.evaluate(2))
print("Polynomial 2 at x=2:", p2.evaluate(2))

# Add the polynomials
p3 = p1.add(p2)
print("Polynomial 1 + Polynomial 2:", p3)

# Multiply the polynomials
p4 = p1.multiply(p2)
print("Polynomial 1 * Polynomial 2:", p4)

# Find the roots of polynomial 1
roots = p1.find_roots()
print("Roots of Polynomial 1:", roots)
