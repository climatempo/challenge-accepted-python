import sys
import os

# Add the path to your project directory
sys.path.append(os.path.abspath('.'))

import unittest
from src.plot_utils import plot_2_graphs
import pandas as pd
import matplotlib.pyplot as plt

class TestPlotUtils(unittest.TestCase):

    def test_plot_2_graphs(self):
        # Test if the function runs without errors
        df = pd.DataFrame({
            'observed': [20, 22, 25, 27, 23],
            'predicted': [18, 21, 24, 26, 22],
            'error': [2, 1, 1, 1, 1]
        }, index=pd.date_range(start='2023-10-20', periods=5, freq='D'))

        try:
            plot_2_graphs(df)
            plt.close()
        except Exception as e:
            self.fail(f"plot_2_graphs raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
