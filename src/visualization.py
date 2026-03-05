import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from shapely.geometry import Polygon


def plot_laydown_zone(zone: Polygon, placements: list, title="Laydown Plan"):
    """
    Plot an irregular polygon zone with placed object footprints.

    Args:
        zone: Shapely Polygon (the laydown perimeter).
        placements: list of dicts from PlacementOptimizer.place_objects().
        title: chart title.
    """
    fig, ax = plt.subplots(figsize=(12, 10))

    zx, zy = zone.exterior.xy
    ax.fill(zx, zy, alpha=0.1, fc='green', ec='black', linewidth=2, label='Zone')

    colors = plt.cm.tab20.colors
    for i, p in enumerate(placements):
        fp = p['object'].get_footprint(p['x'], p['y'], p['rotation'])
        fx, fy = fp.exterior.xy
        color = colors[i % len(colors)]
        ax.fill(fx, fy, alpha=0.6, fc=color, ec='black', linewidth=0.8)
        cx, cy = fp.centroid.x, fp.centroid.y
        ax.text(cx, cy, p['object'].name, ha='center', va='center', fontsize=7)

    ax.set_aspect('equal')
    ax.set_title(title)
    ax.set_xlabel('Easting (m)')
    ax.set_ylabel('Northing (m)')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_laydown(data, labels):
    """Plot a 2D laydown chart.
    Args:
        data (list of tuples): A list of (x, y) coordinates for the plot.
        labels (list of str): Labels for the data points.
    """
    x, y = zip(*data)
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.title('2D Laydown Plot')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    for i, label in enumerate(labels):
        plt.annotate(label, (x[i], y[i]))
    plt.grid()
    plt.show()


def plot_timeline(events):
    """Plot a timeline chart.
    Args:
        events (list of tuples): A list of (date, event) tuples.
    """
    dates, labels = zip(*events)
    plt.figure(figsize=(10, 6))
    plt.plot(dates, range(len(dates)), marker='o')
    plt.title('Timeline Chart')
    plt.yticks(range(len(dates)), labels)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=1))
    plt.grid()
    plt.xticks(rotation=45)
    plt.show()