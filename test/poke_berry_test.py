import os
import unittest
from unittest.mock import patch
import matplotlib
from starlette.testclient import TestClient
from fastapi import HTTPException

from api.route.route_poke import app

matplotlib.use("Agg")


class TestPokeBerry(unittest.TestCase):
    """
    Class that contains test for Poke Berries Module.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initial configuration for Poke Berries module tests.
        """
        cls.client = TestClient(app)

    def test_get_berries_statistics(self):
        """
        Test getting Poke Berries Statistics.
        """
        response = self.client.get("/allBerryStats")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.json()["berries_names"]), int(os.getenv("TOTAL_COUNT_BERRIES"))
        )
        self.assertEqual(response.json()["min_growth_time"], "2 hours")
        self.assertEqual(response.json()["median_growth_time"], "15.0 hours")
        self.assertEqual(response.json()["max_growth_time"], "24 hours")
        self.assertEqual(response.json()["variance_growth_time"], "61.5 hours")
        self.assertEqual(response.json()["mean_growth_time"], "12.86 hours")
        self.assertEqual(response.json()["frequency_growth_time"], "18 hours")

    def test_plot_berries_statistics(self):
        """
        Test plot Poke Berries Statistics.
        """
        response = self.client.get("/allBerryStatsPlot")
        self.assertEqual(response.status_code, 200)

    @patch("db.repository.berries.get_berries")
    def test_get_berries_statistics_error(self, mock_get_berries_statistics):
        """
        Test getting Poke Berries Statistics Error.
        """
        mock_get_berries_statistics.side_effect = HTTPException(500)
        response = self.client.get("/allBerryStats")
        self.assertEqual(response.status_code, 500)

        mock_get_berries_statistics.side_effect = Exception("Poke Berry Error")
        response = self.client.get("/allBerryStats")
        self.assertEqual(response.status_code, 500)

    @patch("db.repository.berries.get_berries")
    def test_plot_berries_statistics_error(self, mock_plot_berries_statistics):
        """
        Test Plot Poke Berries Statistics Error.
        """
        mock_plot_berries_statistics.side_effect = HTTPException(500)
        response = self.client.get("/allBerryStatsPlot")
        self.assertEqual(response.status_code, 500)

        mock_plot_berries_statistics.side_effect = Exception("Poke Berry Error")
        response = self.client.get("/allBerryStatsPlot")
        self.assertEqual(response.status_code, 500)
