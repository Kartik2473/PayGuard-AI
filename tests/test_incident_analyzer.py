import unittest

from incident_analyzer import analyze_incident
from log_processor import process_logs, classify_severity


# ==========================================
# TEST 1: LOG PROCESSING
# ==========================================

class TestLogProcessor(unittest.TestCase):

    def test_log_processing(self):

        logs = """2026-11-19 10:00:01 INFO [payment-service] Service started
2026-11-19 10:00:02 ERROR [payment-service] Payment failed"""

        result = process_logs(logs)

        self.assertEqual(result["total_events"], 2)
        self.assertEqual(len(result["errors"]), 1)

    def test_empty_logs(self):

        result = process_logs("")

        self.assertEqual(result["total_events"], 0)
        self.assertEqual(result["errors"], [])

    def test_unknown_text_is_not_misclassified_as_error(self):

        logs = """Unknown error occurred
Something went wrong during payment"""

        result = process_logs(logs)

        self.assertEqual(result["total_events"], 2)
        self.assertEqual(len(result["errors"]), 0)

        for event in result["events"]:
            self.assertEqual(event["level"], "UNKNOWN")


# ==========================================
# TEST 2: SEVERITY CLASSIFICATION
# ==========================================

class TestSeverityClassification(unittest.TestCase):

    def test_critical_severity(self):

        logs = """2026-11-19 10:00:01 CRITICAL Payment service unavailable"""

        result = process_logs(logs)
        severity = classify_severity(result)

        self.assertEqual(severity["severity"], "CRITICAL")

    def test_high_severity_multiple_errors(self):

        logs = """2026-11-19 10:00:01 ERROR Payment API failed
2026-11-19 10:00:02 ERROR Database query failed
2026-11-19 10:00:03 ERROR Payment processing failed"""

        result = process_logs(logs)
        severity = classify_severity(result)

        self.assertEqual(severity["severity"], "HIGH")

    def test_medium_severity_single_error(self):

        logs = """2026-11-19 10:00:01 ERROR Authentication failed"""

        result = process_logs(logs)
        severity = classify_severity(result)

        self.assertEqual(severity["severity"], "MEDIUM")

    def test_low_severity_warning_only(self):

        logs = """2026-11-19 10:00:01 WARNING Retry limit approaching"""

        result = process_logs(logs)
        severity = classify_severity(result)

        self.assertEqual(severity["severity"], "LOW")

    def test_low_severity_no_failures(self):

        logs = """2026-11-19 10:00:01 INFO Payment service started"""

        result = process_logs(logs)
        severity = classify_severity(result)

        self.assertEqual(severity["severity"], "LOW")


# ==========================================
# TEST 3: INCIDENT ANALYSIS
# ==========================================

class TestIncidentAnalyzer(unittest.TestCase):

    def test_incident_analysis_output(self):

        logs = """2026-11-19 10:00:01 ERROR [payment-service] Payment API timeout"""

        report = analyze_incident(logs)

        self.assertIn("severity", report)
        self.assertIn("likely_causes", report)
        self.assertIn("recommendations", report)
        self.assertIn("escalation", report)
        self.assertIn("timeline", report)
        self.assertIn("correlations", report)

    def test_authentication_failure_detection(self):

        logs = """2026-11-19 10:00:01 ERROR [auth-service] Authentication failed: invalid token"""

        report = analyze_incident(logs)

        cause_names = [
            item["cause"]
            for item in report["likely_causes"]
        ]

        self.assertIn(
            "Authentication or authorization failure",
            cause_names
        )

    def test_evidence_traceability(self):

        logs = """2026-11-19 10:00:01 ERROR [auth-service] Authentication failed: invalid token"""

        report = analyze_incident(logs)

        evidence = report["likely_causes"][0]["evidence"]

        self.assertTrue(len(evidence) > 0)
        self.assertEqual(evidence[0]["line_number"], 1)
        self.assertIn("invalid token", evidence[0]["message"])


# ==========================================
# TEST EXECUTION
# ==========================================

if __name__ == "__main__":

    unittest.main(verbosity=2)