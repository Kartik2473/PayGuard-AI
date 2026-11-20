from pathlib import Path

from log_processor import process_logs, classify_severity
from correlation_engine import generate_correlation_report


# --------------------------------------------------
# ROOT CAUSE PATTERNS
# --------------------------------------------------

ROOT_CAUSE_PATTERNS = [
    {
        "keywords": [
            "timeout",
            "timed out",
            "request timeout",
            "response timeout"
        ],
        "cause": "Payment API or service timeout",
        "recommendations": [
            "Check payment API response time and latency.",
            "Verify API gateway timeout configuration.",
            "Check downstream service availability."
        ]
    },
    {
        "keywords": [
            "connection failed",
            "connection refused",
            "database unavailable",
            "connection error",
            "database connection",
            "db connection",
            "connection lost"
        ],
        "cause": "Database or network connection failure",
        "recommendations": [
            "Verify database server availability.",
            "Check database connection pool utilization.",
            "Review network connectivity and database credentials."
        ]
    },
    {
        "keywords": [
            "authentication",
            "unauthorized",
            "invalid token",
            "token expired",
            "access denied",
            "forbidden"
        ],
        "cause": "Authentication or authorization failure",
        "recommendations": [
            "Validate authentication tokens and expiry.",
            "Review authentication service logs.",
            "Verify authorization configuration."
        ]
    },
    {
        "keywords": [
            "service unavailable",
            "service down",
            "service not responding",
            "health check failed"
        ],
        "cause": "Payment service availability issue",
        "recommendations": [
            "Check payment service health.",
            "Review service restart and deployment history.",
            "Verify application monitoring alerts."
        ]
    },
    {
        "keywords": [
            "insufficient funds",
            "payment declined",
            "transaction declined",
            "payment rejected"
        ],
        "cause": "Payment rejection or transaction failure",
        "recommendations": [
            "Verify payment response codes.",
            "Check transaction status with the payment provider.",
            "Confirm whether the payment rejection is expected."
        ]
    }
]


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def normalize_message(message):
    """Normalize log messages for consistent pattern matching."""

    if not isinstance(message, str):
        return ""

    return " ".join(message.lower().strip().split())


def identify_affected_services(events):
    """Identify unique services associated with failure events."""

    services = {
        event.get("service", "Unknown")
        for event in events
        if event.get("service", "Unknown") != "Unknown"
    }

    return sorted(services)


def calculate_confidence(matching_events):
    """
    Estimate confidence using matching evidence.

    This is a rule-based indicator, not a statistical
    probability or an AI-generated certainty score.
    """

    if not matching_events:
        return "Low"

    critical_count = sum(
        1 for event in matching_events
        if event.get("level", "").upper() in ["CRITICAL", "FATAL"]
    )

    error_count = sum(
        1 for event in matching_events
        if event.get("level", "").upper() == "ERROR"
    )

    if critical_count > 0 or len(matching_events) >= 3:
        return "High"

    if error_count > 0 or len(matching_events) >= 2:
        return "Medium"

    return "Low"


def identify_likely_causes(events):
    """
    Identify potential root causes using log evidence.

    Both warnings and failure events are considered.
    Each finding retains its original log evidence.
    """

    likely_causes = []

    for pattern in ROOT_CAUSE_PATTERNS:

        matching_events = []

        for event in events:

            message = normalize_message(
                event.get("message", "")
            )

            matched_keywords = [
                keyword
                for keyword in pattern["keywords"]
                if keyword in message
            ]

            if matched_keywords:

                matching_events.append({
                    "line_number": event.get("line_number"),
                    "log_level": event.get("level", "UNKNOWN"),
                    "service": event.get("service", "Unknown"),
                    "message": event.get("message", ""),
                    "matched_keywords": matched_keywords
                })

        if matching_events:

            likely_causes.append({
                "cause": pattern["cause"],
                "confidence": calculate_confidence(
                    matching_events
                ),
                "evidence_count": len(matching_events),
                "evidence": matching_events
            })

    if not likely_causes:

        likely_causes.append({
            "cause": "No specific failure pattern identified",
            "confidence": "Low",
            "evidence_count": 0,
            "evidence": []
        })

    return likely_causes


def generate_recommendations(likely_causes):
    """Generate prioritized troubleshooting recommendations."""

    recommendations = []

    for cause in likely_causes:

        if not cause["evidence"]:
            continue

        for pattern in ROOT_CAUSE_PATTERNS:

            if pattern["cause"] == cause["cause"]:

                for recommendation in pattern["recommendations"]:

                    recommendations.append({
                        "priority": (
                            "High"
                            if cause["confidence"] == "High"
                            else "Medium"
                        ),
                        "related_cause": cause["cause"],
                        "action": recommendation
                    })

                break

    # Remove duplicate actions while preserving order.
    unique_recommendations = []
    seen = set()

    for item in recommendations:

        action = item["action"]

        if action not in seen:
            seen.add(action)
            unique_recommendations.append(item)

    if not unique_recommendations:

        unique_recommendations.append({
            "priority": "Medium",
            "related_cause": "General investigation",
            "action": "Review application logs and monitoring metrics."
        })

    return unique_recommendations


def generate_escalation_guidance(severity):

    escalation_rules = {
        "CRITICAL": (
            "Immediately escalate to L2/L3 and the "
            "incident management team."
        ),
        "HIGH": (
            "Escalate to L2 support for urgent investigation."
        ),
        "MEDIUM": (
            "L1 support should investigate and escalate "
            "if unresolved."
        ),
        "LOW": (
            "L1 support can monitor and investigate "
            "if the issue persists."
        )
    }

    return escalation_rules.get(
        severity,
        "Review the incident and follow the standard support process."
    )


# --------------------------------------------------
# MAIN INCIDENT ANALYSIS
# --------------------------------------------------

def analyze_incident(log_text):

    if not isinstance(log_text, str):
        raise TypeError("Log input must be a string.")

    if not log_text.strip():
        raise ValueError("No log data provided for analysis.")

    # Step 1: Process raw logs.
    results = process_logs(log_text)

    # Step 2: Classify incident severity.
    severity_result = classify_severity(results)

    severity = severity_result["severity"]
    severity_reason = severity_result["reason"]

    # Step 3: Retrieve processed events.
    all_events = results.get("events", [])

    failure_events = (
        results.get("errors", [])
        + results.get("critical", [])
    )

    # Step 4: Identify affected services.
    affected_services = identify_affected_services(
        failure_events
    )

    # Step 5: Identify potential root causes.
    # Warnings are included because they may contain
    # early indicators of an incident.
    likely_causes = identify_likely_causes(all_events)

    # Step 6: Generate troubleshooting recommendations.
    recommendations = generate_recommendations(
        likely_causes
    )

    # Step 7: Generate escalation guidance.
    escalation = generate_escalation_guidance(severity)

    # Step 8: Generate event correlation report.
    correlation_report = generate_correlation_report(
        all_events
    )

    # Step 9: Generate unified incident report.
    report = {
        "severity": severity,
        "severity_reason": severity_reason,

        "total_logs": results.get("total_lines", 0),
        "total_events": results.get("total_events", 0),

        "critical_events": len(results.get("critical", [])),
        "errors": len(results.get("errors", [])),
        "warnings": len(results.get("warnings", [])),

        "affected_services": affected_services,

        "likely_causes": likely_causes,
        "recommendations": recommendations,

        "escalation": escalation,

        "timeline": correlation_report.get("timeline", []),
        "correlations": correlation_report.get(
            "correlations",
            {
                "transaction_groups": {},
                "service_groups": {},
                "repeated_errors": {}
            }
        )
    }

    return report


# --------------------------------------------------
# CONSOLE REPORT DISPLAY
# --------------------------------------------------

def display_report(report):

    print("\n" + "=" * 55)
    print("          PAYGUARD AI INCIDENT REPORT")
    print("=" * 55)

    # Incident overview.
    print("\n1. INCIDENT OVERVIEW")

    print("Severity:", report["severity"])
    print("Severity Reason:", report["severity_reason"])
    print("Total Logs:", report["total_logs"])
    print("Total Events:", report["total_events"])

    # Incident statistics.
    print("\n2. INCIDENT STATISTICS")

    print("Critical Events:", report["critical_events"])
    print("Errors:", report["errors"])
    print("Warnings:", report["warnings"])

    # Affected services.
    print("\n3. AFFECTED SERVICES")

    if report["affected_services"]:

        for service in report["affected_services"]:
            print("-", service)

    else:
        print("No affected services identified.")

    # Likely causes.
    print("\n4. LIKELY CAUSES AND EVIDENCE")

    for item in report["likely_causes"]:

        print("\nLikely Cause:", item["cause"])
        print("Confidence:", item["confidence"])
        print("Evidence Count:", item["evidence_count"])

        if item["evidence"]:

            for evidence in item["evidence"]:

                print("\n  Line:", evidence["line_number"])
                print("  Level:", evidence["log_level"])
                print("  Service:", evidence["service"])
                print("  Original Log:", evidence["message"])

        else:

            print("  No supporting failure event found.")

    # Recommendations.
    print("\n5. TROUBLESHOOTING RECOMMENDATIONS")

    for recommendation in report["recommendations"]:

        print(
            f"[{recommendation['priority']}] "
            f"{recommendation['action']}"
        )

        print(
            "  Related Cause:",
            recommendation["related_cause"]
        )

    # Escalation.
    print("\n6. ESCALATION GUIDANCE")

    print(report["escalation"])

    # Timeline.
    print("\n7. INCIDENT TIMELINE")

    if report["timeline"]:

        for event in report["timeline"]:

            print(
                event.get("display_time", "Unknown"),
                "|",
                event.get("level", "UNKNOWN"),
                "|",
                event.get("service", "Unknown"),
                "|",
                event.get("message", "")
            )

    else:

        print("No timeline information available.")

    # Correlation report.
    correlations = report["correlations"]

    print("\n8. PAYMENT / TRANSACTION REFERENCES")

    transaction_groups = correlations.get(
        "transaction_groups", {}
    )

    if transaction_groups:

        for reference, events in transaction_groups.items():

            print("Reference:", reference)
            print("Related Events:", len(events))

    else:

        print("No payment or transaction references found.")

    # Service correlations.
    print("\n9. SERVICE CORRELATION")

    service_groups = correlations.get(
        "service_groups", {}
    )

    if service_groups:

        for service, events in service_groups.items():

            print(service, ":", len(events), "events")

    else:

        print("No service correlations detected.")

    # Repeated errors.
    print("\n10. REPEATED ERROR PATTERNS")

    repeated_errors = correlations.get(
        "repeated_errors", {}
    )

    if repeated_errors:

        for pattern, events in repeated_errors.items():

            print("Error:", pattern)
            print("Occurrences:", len(events))

    else:

        print("No repeated error patterns detected.")

    print("\n" + "=" * 55)
    print("End of Incident Report")
    print("=" * 55)


# --------------------------------------------------
# SCRIPT EXECUTION
# --------------------------------------------------

if __name__ == "__main__":

    sample_log_path = (
        Path(__file__).resolve().parent
        / "sample_logs"
        / "payment_logs.txt"
    )

    try:

        logs = sample_log_path.read_text(encoding="utf-8")

        if not logs.strip():

            print("No log data found in the sample file.")

        else:

            report = analyze_incident(logs)
            display_report(report)

    except FileNotFoundError:

        print(
            "Error: Sample log file not found:",
            sample_log_path
        )

    except (TypeError, ValueError) as error:

        print("Input validation error:", error)

    except Exception as error:

        print("Incident analysis failed:", error)
        raise