import time
from time import perf_counter, sleep
import numpy as np
import csv

# --- Matplotlib 2D live plot test ---
def test_matplotlib(num_frames=300, target_hz=20):
    import matplotlib.pyplot as plt

    period = 1.0 / target_hz
    t0 = perf_counter()
    times_render = []
    lags = []

    plt.ion()
    fig, ax = plt.subplots()
    x = np.arange(0, 200)
    y1 = np.zeros_like(x, dtype=float)
    y2 = np.zeros_like(x, dtype=float)
    ln1, = ax.plot(x, y1, label="Strain")
    ln2, = ax.plot(x, y2, label="Temperature")
    ax.legend()
    fig.canvas.draw()
    fig.canvas.flush_events()

    for i in range(num_frames):
        frame_start = perf_counter()
        # --- simulate incoming sensor data ---
        y1 = 0.9*np.sin(2*np.pi*(i/50.0) + (x/40.0)) + np.random.normal(0, 0.03, x.size)
        y2 = 25 + 2*np.sin(2*np.pi*(i/80.0) + (x/60.0))

        # --- update plot (render timing) ---
        render_start = perf_counter()
        ln1.set_ydata(y1)
        ln2.set_ydata(y2)
        ax.relim(); ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()
        render_end = perf_counter()

        times_render.append((render_end - render_start) * 1000.0)  # ms
        lags.append((render_end - frame_start) * 1000.0)           # ms

        # keep near target rate
        elapsed = perf_counter() - frame_start
        if elapsed < period:
            sleep(period - elapsed)
    plt.savefig("matplotlib_plot.png", dpi=300)
    plt.ioff()
    plt.close(fig)

    avg_render = float(np.mean(times_render))
    fps = 1000.0 / avg_render if avg_render > 0 else float('inf')
    avg_lag = float(np.mean(lags))
    return {"Library": "Matplotlib", "Avg Render (ms)": round(avg_render, 2), "FPS": round(fps, 2), "Lag (ms)": round(avg_lag, 2)}

# --- PyVista 3D deformation test ---
def test_pyvista(num_frames=300, target_hz=20):
    import pyvista as pv
    from time import perf_counter, sleep
    import numpy as np

    period = 1.0 / target_hz
    times_render, lags = [], []

    mesh = pv.ParametricEllipsoid(1.0, 0.35, 0.18)  # rudder-like shape
    plotter = pv.Plotter(off_screen=False, window_size=[800, 600])
    plotter.add_text("PyVista 3D Deformation", font_size=12)
    actor = plotter.add_mesh(mesh, smooth_shading=True)

    # create the window/context once
    plotter.show(auto_close=False, interactive_update=True)

    base_pts = mesh.points.copy()

    for i in range(num_frames):
        frame_start = perf_counter()

        # small z-deformation ripple over time
        pts = base_pts.copy()
        pts[:, 2] = pts[:, 2] + 0.02 * np.sin(0.2 * i + pts[:, 0] * 6.0)
        mesh.points = pts              # assigning points is enough to flag an update
        # mesh.Modified()              # (optional) if you prefer to be explicit

        render_start = perf_counter()
        plotter.render()
        render_end = perf_counter()

        times_render.append((render_end - render_start) * 1000.0)
        lags.append((render_end - frame_start) * 1000.0)

        elapsed = perf_counter() - frame_start
        if elapsed < period:
            sleep(period - elapsed)

    plotter.screenshot("pyvista_deformation.png")
    plotter.close()

    import numpy as np
    avg_render = float(np.mean(times_render))
    fps = 1000.0 / avg_render if avg_render > 0 else float("inf")
    avg_lag = float(np.mean(lags))
    return {
        "Library": "PyVista",
        "Avg Render (ms)": round(avg_render, 2),
        "FPS": round(fps, 2),
        "Lag (ms)": round(avg_lag, 2),
    }


def save_results_csv(results, path="viz_results.csv"):
    keys = ["Library", "Avg Render (ms)", "FPS", "Lag (ms)"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for row in results:
            w.writerow(row)
    return path

def main():
    print("Running Matplotlib test...")
    r1 = test_matplotlib(num_frames=300, target_hz=20)
    print(r1)

    print("Running PyVista test...")
    r2 = test_pyvista(num_frames=300, target_hz=20)
    print(r2)

    results = [r1, r2]
    csv_path = save_results_csv(results)
    print("\n=== SUMMARY ===")
    for r in results:
        print(f"{r['Library']}: Avg Render={r['Avg Render (ms)']} ms | FPS={r['FPS']} | Lag={r['Lag (ms)']} ms")
    print(f"\nSaved CSV -> {csv_path}")

if __name__ == "__main__":
    main()
