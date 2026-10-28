import tempfile
import unittest
from pathlib import Path

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from research_analyzer.dataset import Dataset
from research_analyzer.visualization import (
    plot_boxplot,
    plot_correlation_heatmap,
    plot_distribution,
)


@unittest.skipUnless(MATPLOTLIB_AVAILABLE, "matplotlib visualization extra is not installed")
class TestDatasetVisualization(unittest.TestCase):
    def setUp(self):
        self.dataset = Dataset("unused.csv")
        self.dataset.data = [
            {"Age": "20", "Study_Hours": "2", "Final_Score": "70"},
            {"Age": "21", "Study_Hours": "4", "Final_Score": "80"},
            {"Age": "22", "Study_Hours": "6", "Final_Score": "90"},
        ]

    def tearDown(self):
        if MATPLOTLIB_AVAILABLE:
            plt.close("all")

    def test_distribution_plot_has_title_and_axis_labels(self):
        figure = plot_distribution(self.dataset, "Study_Hours")
        self.assertEqual(figure.axes[0].get_title(), "Distribution of Study_Hours")
        self.assertEqual(figure.axes[0].get_xlabel(), "Study_Hours")
        self.assertEqual(figure.axes[0].get_ylabel(), "Frequency")

    def test_boxplot_compares_requested_columns(self):
        figure = plot_boxplot(self.dataset, ["Age", "Final_Score"])
        self.assertEqual(
            [tick.get_text() for tick in figure.axes[0].get_xticklabels()],
            ["Age", "Final_Score"],
        )

    def test_correlation_heatmap_uses_requested_columns(self):
        figure = plot_correlation_heatmap(
            self.dataset, ["Study_Hours", "Final_Score"]
        )
        self.assertEqual(figure.axes[0].get_title(), "Pearson Correlation Heatmap")
        self.assertEqual(len(figure.axes[0].get_xticklabels()), 2)

    def test_plot_can_be_saved_to_a_new_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "nested" / "distribution.png"
            plot_distribution(self.dataset, "Age", output)
            self.assertTrue(output.is_file())
            self.assertGreater(output.stat().st_size, 0)

    def test_distribution_rejects_column_without_numeric_values(self):
        self.dataset.data = [{"Age": ""}, {"Age": "  "}]
        with self.assertRaisesRegex(ValueError, "no numeric values"):
            plot_distribution(self.dataset, "Age")

    def test_boxplot_requires_at_least_one_column(self):
        with self.assertRaisesRegex(ValueError, "at least one"):
            plot_boxplot(self.dataset, [])

    def test_heatmap_requires_two_columns(self):
        with self.assertRaisesRegex(ValueError, "at least two"):
            plot_correlation_heatmap(self.dataset, ["Age"])


if __name__ == "__main__":
    unittest.main()
