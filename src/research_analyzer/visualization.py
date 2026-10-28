"""Optional plotting helpers for exploratory dataset analysis.

Install the plotting extra with: python -m pip install -e ".[visualization]"
"""
from pathlib import Path


def _pyplot():
    """Import matplotlib lazily so core CSV/statistics features stay lightweight."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "Plotting requires matplotlib. Install it with "
            'python -m pip install -e ".[visualization]".'
        ) from exc
    return plt


def _finish_figure(figure, output_path):
    """Optionally save a figure and always return it for further customization."""
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(path, bbox_inches="tight")
    return figure


def plot_distribution(dataset, column, output_path=None):
    """Plot a histogram for one numeric dataset column and return its figure."""
    values = dataset.get_column_values(column)
    if not values:
        raise ValueError(f"Column {column!r} has no numeric values to plot.")

    plt = _pyplot()
    figure, axis = plt.subplots()
    axis.hist(values, bins="auto", edgecolor="black")
    axis.set_title(f"Distribution of {column}")
    axis.set_xlabel(column)
    axis.set_ylabel("Frequency")
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    return _finish_figure(figure, output_path)


def plot_boxplot(dataset, columns, output_path=None):
    """Compare numeric columns with a box plot and return its figure."""
    if isinstance(columns, str):
        columns = [columns]
    columns = list(columns)
    if not columns:
        raise ValueError("Provide at least one numeric column to plot.")

    data = []
    labels = []
    for column in columns:
        values = dataset.get_column_values(column)
        if not values:
            raise ValueError(f"Column {column!r} has no numeric values to plot.")
        data.append(values)
        labels.append(column)

    plt = _pyplot()
    figure, axis = plt.subplots()
    axis.boxplot(data, tick_labels=labels)
    axis.set_title("Numeric Column Distributions")
    axis.set_ylabel("Value")
    axis.grid(axis="y", alpha=0.25)
    figure.tight_layout()
    return _finish_figure(figure, output_path)


def plot_correlation_heatmap(dataset, columns=None, output_path=None):
    """Plot pairwise Pearson correlations for numeric columns and return figure."""
    if columns is None:
        columns = dataset.get_numeric_columns()
    else:
        columns = list(columns)

    if len(columns) < 2:
        raise ValueError("A correlation heatmap requires at least two numeric columns.")

    matrix = []
    for first in columns:
        row = []
        for second in columns:
            correlation = dataset.correlation(first, second)
            row.append(float("nan") if correlation is None else correlation)
        matrix.append(row)

    plt = _pyplot()
    figure, axis = plt.subplots()
    image = axis.imshow(matrix, vmin=-1, vmax=1, cmap="coolwarm")
    axis.set_xticks(range(len(columns)), labels=columns, rotation=45, ha="right")
    axis.set_yticks(range(len(columns)), labels=columns)
    axis.set_title("Pearson Correlation Heatmap")
    figure.colorbar(image, ax=axis, label="Pearson r")
    figure.tight_layout()
    return _finish_figure(figure, output_path)
