import numpy as np
import sympy as sp
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

max_iter=100

def secant_minimization(fx, a, b, tol=1e-4):
    x = sp.symbols('x')
    f = sp.sympify(fx, evaluate=False)  # Ensure proper function handling
    df = sp.diff(f, x)  # Compute the derivative

    f_lambda = sp.lambdify(x, f, 'numpy')
    df_lambda = sp.lambdify(x, df, 'numpy')

    results = []
    L, R = a, b
    iterations = 0
    graph_images = []
    z = None  # Initialize z to avoid reference error if while loop doesn't execute

    while iterations < max_iter:
        f_L = float(df.subs(x, L))
        f_R = float(df.subs(x, R))

        if f_L < 0 and f_R > 0:
            z = R - ((f_R * (R - L)) / (f_R - f_L))
            f_z = float(df.subs(x, z))

            results.append({
                "iteration": iterations + 1,
                "L": float(L),
                "R": float(R),
                "z": float(z),
                "f'(L)": f_L,
                "f'(R)": f_R,
                "f'(z)": f_z
            })

            # Generate graph for this iteration
            try:
                graph_images.append(generate_iteration_graph(f_lambda, float(L), float(R), float(z), iterations))
            except Exception as e:
                # Handle any plotting errors gracefully
                graph_images.append(None)
                print(f"Error generating graph for iteration {iterations}: {e}")

            if f_z < 0:
                L = z
            else:
                R = z

            if abs(f_z) <= tol:
                break
        else:
            # Handle the case where f_L and f_R don't bracket a root
            print(f"Warning: The derivative values at bounds do not bracket zero: f'({L})={f_L}, f'({R})={f_R}")
            break

        iterations += 1

    if z is None:
        # If no solution was found, use midpoint as a fallback
        z = (L + R) / 2
        
    return {
        "x_min": float(z),
        "f_min": float(f.subs(x, z)),
        "iterations": results,
        "graphs": [img for img in graph_images if img is not None]  # Only return valid graph images
    }


def generate_iteration_graph(f, a, b, x_min, iteration):
    """Generates a graph showing function f(x), bounds a & b, and the current minimum x_min."""
    try:
        # Create more points near the significant areas
        x_vals = np.linspace(a - 0.5, b + 0.5, 1000)
        
        # Evaluate function carefully to avoid complex numbers
        y_vals = []
        for xi in x_vals:
            try:
                yi = f(xi)
                # Check if result is complex or contains infinities
                if np.iscomplex(yi) or not np.isfinite(yi):
                    y_vals.append(np.nan)
                else:
                    y_vals.append(float(yi))
            except:
                y_vals.append(np.nan)
        
        y_vals = np.array(y_vals)
        
        # Remove NaN values for plotting
        mask = ~np.isnan(y_vals)
        x_plot = x_vals[mask]
        y_plot = y_vals[mask]
        
        # Evaluate f(x_min) carefully
        try:
            f_min = float(f(x_min))
            if np.iscomplex(f_min) or not np.isfinite(f_min):
                f_min = np.nan
        except:
            f_min = np.nan

        plt.figure(figsize=(6, 4))
        
        if len(x_plot) > 0:  # Only plot if we have valid points
            plt.plot(x_plot, y_plot, label='f(x)', color='blue')
        
        plt.axvline(a, color='red', linestyle="--", label="a (Lower Bound)")
        plt.axvline(b, color='green', linestyle="--", label="b (Upper Bound)")
        
        if not np.isnan(f_min):
            plt.scatter([x_min], [f_min], color='purple', label="Current Min", zorder=5)

        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title(f'Iteration {iteration + 1}')
        plt.legend()
        plt.grid(True)
        
        # Set y-axis limits to focus on the important region
        plt.ylim(bottom=min(y_plot) if len(y_plot) > 0 else None, 
                top=max(y_plot) + 10 if len(y_plot) > 0 else None)
        
        # Convert plot to base64 image
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        encoded_string = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
        plt.close()

        return f"data:image/png;base64,{encoded_string}"
    except Exception as e:
        plt.close()  # Make sure to close the figure in case of error
        raise e


def generate_graph(fx, x_min):
    """Generates the final function graph after minimization."""
    x = sp.symbols('x')
    f = sp.sympify(fx, evaluate=False)
    df = sp.diff(f, x)  # First derivative

    f_lambda = sp.lambdify(x, f, 'numpy')
    df_lambda = sp.lambdify(x, df, 'numpy')

    try:
        # Generate a range of x values, focused around x_min
        x_vals = np.linspace(max(0.1, x_min - 2), x_min + 2, 500)
        
        # Evaluate function and derivative carefully
        y_vals = []
        dy_vals = []
        
        for xi in x_vals:
            try:
                yi = float(f_lambda(xi))
                dyi = float(df_lambda(xi))
                
                if np.iscomplex(yi) or not np.isfinite(yi):
                    y_vals.append(np.nan)
                else:
                    y_vals.append(yi)
                    
                if np.iscomplex(dyi) or not np.isfinite(dyi):
                    dy_vals.append(np.nan)
                else:
                    dy_vals.append(dyi)
            except:
                y_vals.append(np.nan)
                dy_vals.append(np.nan)
        
        y_vals = np.array(y_vals)
        dy_vals = np.array(dy_vals)
        
        # Get non-NaN values for plotting
        mask_y = ~np.isnan(y_vals)
        mask_dy = ~np.isnan(dy_vals)
        
        # Carefully evaluate at minimum
        try:
            f_min = float(f_lambda(x_min))
            df_min = float(df_lambda(x_min))
            
            if np.iscomplex(f_min) or not np.isfinite(f_min):
                f_min = np.nan
            if np.iscomplex(df_min) or not np.isfinite(df_min):
                df_min = np.nan
        except:
            f_min = np.nan
            df_min = np.nan

        plt.figure(figsize=(12, 6))

        # Function Plot
        plt.subplot(1, 2, 1)
        if np.any(mask_y):
            plt.plot(x_vals[mask_y], y_vals[mask_y], label="f(x)", color='b')
        if not np.isnan(f_min):
            plt.scatter([x_min], [f_min], color='r', marker='o', label="Min Point")
        plt.title("Function Curve")
        plt.xlabel("x")
        plt.ylabel("f(x)")
        plt.legend()
        plt.grid()

        # Derivative Plot
        plt.subplot(1, 2, 2)
        if np.any(mask_dy):
            plt.plot(x_vals[mask_dy], dy_vals[mask_dy], label="f'(x)", color='g')
        if not np.isnan(df_min):
            plt.scatter([x_min], [df_min], color='r', marker='o', label="Derivative at Min")
        plt.title("Derivative Curve")
        plt.xlabel("x")
        plt.ylabel("f'(x)")
        plt.legend()
        plt.grid()

        # Convert plot to base64 image
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)
        encoded_string = base64.b64encode(buf.getvalue()).decode("utf-8")
        buf.close()
        plt.close()

        return encoded_string
    except Exception as e:
        plt.close()  # Make sure to close the figure
        print(f"Error generating final graph: {e}")
        return ""