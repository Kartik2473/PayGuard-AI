import re
from collections import Counter


# --------------------------------------------------
# LOG PATTERNS
# --------------------------------------------------

LOG_LEVEL_PATTERN = re.compile(
    r"^\s*(?:"
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
    r"(?:Z|[+-]\d{2}:?\d{2})?\s+"
    r")?"
    r"(?:\[[^\]]+\]\s*)?"
    r"(CRITICAL|FATAL|ERROR|WARN(?:ING)?|INFO|DEBUG|TRACE)"
    r"\b",
    re.IGNORECASE
)

TIMESTAMP_PATTERN = re.compile(
    r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?"
    r"(?:Z|[+-]\d{2}:?\d{2})?"
)

SERVICE_PATTERN = re.compile(
    r"\b(payment service|payment-service|payment api|payment-api|"
    r"database|db-service|auth-service|api-gateway)\b",
    re.IGNORECASE
)


# --------------------------------------------------
# LOG PROCESSING
# --------------------------------------------------

def process_logs(log_text):
    """
    Parse raw application logs into structured events.

    Each event contains:
    - Line number
    - Timestamp
    - Log level
    - Service
    - Original log message
    """

    if not isinstance(log_text, str):
        raise TypeError("Log input must be a string.")

    lines = log_text.splitlines()

    events = []
    level_counts = Counter()

    for line_number, line in enumerate(lines, start=1):

        if not line.strip():
            continue

        # Extract log level.
        level_match = LOG_LEVEL_PATTERN.search(line)

        level = (
            level_match.group(1).upper()
            if level_match
            else "UNKNOWN"
        )

        if level == "WARN":
            level = "WARNING"

        # Extract timestamp.
        timestamp_match = TIMESTAMP_PATTERN.search(line)

        timestamp = (
            timestamp_match.group(0)
            if timestamp_match
            else None
        )

        # Extract service name.
        service_match = SERVICE_PATTERN.search(line)

        service = (
            service_match.group(0)
            if service_match
            else "Unknown"
        )

        event = {
            "line_number": line_number,
            "timestamp": timestamp,
            "level": level,
            "service": service,
            "message": line.strip()
        }

        events.append(event)
        level_counts[level] += 1

    # Group events by severity level.
    critical = [
        event for event in events
        if event["level"] in ["CRITICAL", "FATAL"]
    ]

    errors = [
        event for event in events
        if event["level"] == "ERROR"
    ]

    warnings = [
        event for event in events
        if event["level"] == "WARNING"
    ]

    return {
        "total_lines": len(lines),
        "total_events": len(events),
        "events": events,
        "level_counts": dict(level_counts),
        "critical": critical,
        "errors": errors,
        "warnings": warnings
    }


# --------------------------------------------------
# SEVERITY CLASSIFICATION
# --------------------------------------------------

def classify_severity(results):
    """
    Classify incident severity using transparent rules.

    Priority:
    CRITICAL > HIGH > MEDIUM > LOW

    These rules are heuristic and should be reviewed
    against actual business impact.
    """

    critical_events = results.get("critical", [])
    errors = results.get("errors", [])
    warnings = results.get("warnings", [])

    failure_events = critical_events + errors

    failure_messages = [
        event.get("message", "").lower()
        for event in failure_events
    ]

    # Rule 1: Critical or fatal events.
    if critical_events:

        return {
            "severity": "CRITICAL",
            "reason": "Critical or fatal log events detected."
        }

    # Rule 2: Payment service availability failures.
    availability_keywords = [
        "service unavailable",
        "payment service down",
        "payment service unavailable",
        "service not responding"
    ]

    if any(
        keyword in message
        for message in failure_messages
        for keyword in availability_keywords
    ):

        return {
            "severity": "HIGH",
            "reason": "Payment service availability failure detected."
        }

    # Rule 3: Database and network failures.
    database_keywords = [
        "database connection failed",
        "database unavailable",
        "connection refused",
        "connection failed",
        "database connection lost"
    ]

    if any(
        keyword in message
        for message in failure_messages
        for keyword in database_keywords
    ):

        return {
            "severity": "HIGH",
            "reason": "Database or network connectivity failure detected."
        }

    # Rule 4: Multiple application errors.
    if len(errors) >= 3:

        return {
            "severity": "HIGH",
            "reason": "Three or more application errors detected."
        }

    # Rule 5: Individual application errors.
    if errors:

        return {
            "severity": "MEDIUM",
            "reason": "Application errors detected."
        }

    # Rule 6: Warning events.
    if warnings:

        return {
            "severity": "LOW",
            "reason": "Only warning events detected."
        }

    # Rule 7: No significant failures.
    return {
        "severity": "LOW",
        "reason": "No significant failure events detected."
    }