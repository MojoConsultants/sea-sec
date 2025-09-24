import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import pandas as pd
import os
from reporting_service import generate, ReportSummary

# Import the function and dependencies

class DummySecurityEvent:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def model_dump(self):
        return {"id": self.id, "name": self.name}

class TestReportingService(unittest.TestCase):
    @patch("reporting_service.HTML")
    @patch("reporting_service.env")
    @patch("reporting_service.REPORTS_DIR", Path("test_reports"))
    def test_generate_success(self, mock_env, mock_html):
        # Setup
        events = [DummySecurityEvent(1, "event1"), DummySecurityEvent(2, "event2")]
        risk_scores = [0.9, 0.5]
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Report</html>"
        mock_env.get_template.return_value = mock_template
        mock_html.return_value.write_pdf.return_value = None
        mock_html.return_value.write_png.return_value = None

        # Run
        summary = generate(events, risk_scores)

        # Assert
        self.assertIsInstance(summary, ReportSummary)
        self.assertEqual(summary.total_events, 2)
        self.assertEqual(summary.anomalies, 1)
        self.assertTrue(summary.report_html_path.endswith("report.html"))
        self.assertTrue(summary.report_csv_path.endswith("report.csv"))
        self.assertTrue(summary.report_json_path.endswith("report.json"))
        self.assertTrue(summary.report_pdf_path.endswith("report.pdf"))
        self.assertTrue(summary.report_png_path.endswith("report.png"))

    @patch("reporting_service.env")
    @patch("reporting_service.REPORTS_DIR", Path("test_reports"))
    def test_generate_no_events(self, mock_env):
        with self.assertRaises(ValueError):
            generate([], [])

    @patch("reporting_service.HTML")
    @patch("reporting_service.env")
    @patch("reporting_service.REPORTS_DIR", Path("test_reports"))
    def test_generate_png_export_failure(self, mock_env, mock_html):
        events = [DummySecurityEvent(1, "event1")]
        risk_scores = [0.95]
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>Report</html>"
        mock_env.get_template.return_value = mock_template
        mock_html.return_value.write_pdf.return_value = None
        mock_html.return_value.write_png.side_effect = Exception("PNG error")

        summary = generate(events, risk_scores)
        self.assertIsNone(summary.report_png_path)

if __name__ == "__main__":
    unittest.main()