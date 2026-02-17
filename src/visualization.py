import matplotlib.pyplot as plt
import matplotlib.dates as mdates


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