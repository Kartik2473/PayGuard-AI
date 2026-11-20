import re
from datetime import datetime


# Extract transaction IDs from log messages
TRANSACTION_PATTERN = re.compile(
    r"\b(?:transaction_id|transactionId|txn_id|txnId|"
    r"payment_id|paymentId|payment\s+ID)"
    r"\s*[:=]?\s*([A-Za-z0-9_-]+)",
    re.IGNORECASE
)


def extract_transaction_id(message):

    if not isinstance(message, str):
        return None

    match = TRANSACTION_PATTERN.search(message)

    if match:
        return match.group(1)

    return None


def parse_timestamp(timestamp):

    if not timestamp:
        return None

    if not isinstance(timestamp, str):
        return None

    try:
        return datetime.fromisoformat(
            timestamp.replace("Z", "+00:00")
        )
    except ValueError:
        return None


def create_timeline(events):

    timeline = []

    for event in events:

        timestamp = parse_timestamp(
            event.get("timestamp")
        )

        timeline.append({
            "timestamp": timestamp,
            "display_time": event.get("timestamp") or "Unknown time",
            "level": event.get("level", "UNKNOWN"),
            "service": event.get("service", "Unknown"),
            "message": event.get("message", "")
        })

    # Sort events by timestamp.
    # Events without timestamps appear at the end.
    timeline.sort(
        key=lambda item: (
            item["timestamp"] is None,
            item["timestamp"].timestamp()
            if item["timestamp"] is not None
            else 0
        )
    )

    return timeline


def correlate_events(events):

    transaction_groups = {}
    service_groups = {}
    error_patterns = {}

    for event in events:

        message = event.get("message", "")
        service = event.get("service", "Unknown")
        level = event.get("level", "UNKNOWN")

        # Group events using transaction IDs.
        transaction_id = extract_transaction_id(message)

        if transaction_id:

            transaction_groups.setdefault(
                transaction_id, []
            ).append(event)

        # Group events by service.
        if service and service != "Unknown":

            service_groups.setdefault(
                service, []
            ).append(event)

        # Group similar error messages.
        if level in ["ERROR", "CRITICAL", "FATAL"]:

            # Remove timestamps before comparing messages.
            pattern = re.sub(
                r"\d{4}-\d{2}-\d{2}[T ]"
                r"\d{2}:\d{2}:\d{2}(?:\.\d+)?",
                "",
                message.lower()
            ).strip()

            error_patterns.setdefault(
                pattern, []
            ).append(event)

    # Keep only error patterns that occur more than once.
    repeated_errors = {
        pattern: matching_events
        for pattern, matching_events in error_patterns.items()
        if len(matching_events) > 1
    }

    return {
        "transaction_groups": transaction_groups,
        "service_groups": service_groups,
        "repeated_errors": repeated_errors
    }


def generate_correlation_report(events):

    if not isinstance(events, list):
        raise TypeError("Events must be provided as a list.")

    timeline = create_timeline(events)

    correlations = correlate_events(events)

    return {
        "timeline": timeline,
        "correlations": correlations
    }


def display_correlation_report(report):

    print("\nPAYGUARD AI - EVENT CORRELATION")

    print("\n1. INCIDENT TIMELINE")

    if not report["timeline"]:

        print("No events available.")

    for event in report["timeline"]:

        print(
            event["display_time"],
            "|",
            event["level"],
            "|",
            event["service"],
            "|",
            event["message"]
        )

    correlations = report["correlations"]

    print("\n2. TRANSACTION CORRELATION")

    if correlations["transaction_groups"]:

        for transaction_id, events in correlations[
            "transaction_groups"
        ].items():

            print("Transaction ID:", transaction_id)
            print("Related events:", len(events))

    else:

        print("No transaction IDs found in the supplied logs.")

    print("\n3. SERVICE CORRELATION")

    if correlations["service_groups"]:

        for service, events in correlations[
            "service_groups"
        ].items():

            print(service, ":", len(events), "events")

    else:

        print("No service correlations detected.")

    print("\n4. REPEATED ERROR PATTERNS")

    if correlations["repeated_errors"]:

        for pattern, events in correlations[
            "repeated_errors"
        ].items():

            print("Error:", pattern)
            print("Occurrences:", len(events))

    else:

        print("No repeated error patterns detected.")