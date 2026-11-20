import json
import hashlib
from datetime import datetime

import pandas as pd
import streamlit as st

from incident_analyzer import analyze_incident
from ai_engine import analyze_with_ai, is_ai_available


# =========================================================
# 1. PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="PayGuard AI | Incident Analyzer",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# 2. CONSTANTS
# =========================================================

SAMPLE_LOGS = """2026-11-18 10:00:01 INFO Payment service started
2026-11-18 10:00:05 INFO Processing payment ID 1001
2026-11-18 10:00:08 ERROR Payment API timeout
2026-11-18 10:00:10 ERROR Database connection failed
2026-11-18 10:00:12 CRITICAL Payment service unavailable
2026-11-18 10:00:15 WARNING Retry limit approaching
2026-11-18 10:00:20 INFO Monitoring system active"""


SEVERITY_CONFIG = {
    "CRITICAL": {
        "icon": "🔴",
        "color": "#F87171",
        "background": "#351B25",
        "description": "Immediate investigation required."
    },
    "HIGH": {
        "icon": "🟠",
        "color": "#FB923C",
        "background": "#352719",
        "description": "Urgent investigation recommended."
    },
    "MEDIUM": {
        "icon": "🟡",
        "color": "#FACC15",
        "background": "#352F1B",
        "description": "Investigation and monitoring required."
    },
    "LOW": {
        "icon": "🟢",
        "color": "#4ADE80",
        "background": "#173328",
        "description": "Continue normal monitoring."
    }
}


# =========================================================
# 3. SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "log_input": "",
    "incident_report": None,
    "ai_result": None,
    "analysis_timestamp": None,
    "analysis_ai_enabled": False,
    "last_uploaded_signature": None,
    "analysis_error": None,
    "success_message": None,
    "upload_widget_version": 0
}

for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 4. CALLBACK FUNCTIONS
# =========================================================

def reset_analysis():

    st.session_state.incident_report = None
    st.session_state.ai_result = None
    st.session_state.analysis_timestamp = None
    st.session_state.analysis_ai_enabled = False
    st.session_state.analysis_error = None


def load_sample_logs():

    st.session_state.log_input = SAMPLE_LOGS
    st.session_state.last_uploaded_signature = None

    st.session_state.upload_widget_version += 1

    reset_analysis()

    st.session_state.success_message = (
        "Sample logs loaded successfully."
    )


def clear_logs():

    st.session_state.log_input = ""
    st.session_state.last_uploaded_signature = None

    st.session_state.upload_widget_version += 1

    reset_analysis()

    st.session_state.success_message = (
        "Logs and previous analysis cleared."
    )


# =========================================================
# 5. DASHBOARD THEME
# =========================================================

st.markdown("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

.stApp {
    background-color: #0B1120 !important;
    color: #E2E8F0 !important;
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"],
[data-testid="stMain"],
[data-testid="stHeader"] {
    background-color: #0B1120 !important;
}

.main .block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background-color: #080F1D !important;
    border-right: 1px solid #263449;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #F8FAFC !important;
}

section[data-testid="stSidebar"] p {
    color: #A8B5C7 !important;
}

h1, h2, h3, h4, h5 {
    color: #F8FAFC !important;
}

.main-heading {
    font-size: 30px;
    font-weight: 800;
    color: #F8FAFC !important;
}

.main-description {
    color: #A8B5C7 !important;
    font-size: 14px;
}

.section-heading {
    font-size: 21px;
    font-weight: 700;
    color: #F8FAFC !important;
}

[data-testid="stMain"] [data-testid="stMarkdownContainer"] p,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] li {
    color: #D4DCE8 !important;
}

[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    color: #A8B5C7 !important;
}

[data-testid="stMain"] label {
    color: #DCE5F1 !important;
}

[data-testid="stMain"] strong {
    color: #F8FAFC !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #151F32 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

[data-testid="stMetric"] {
    background-color: #151F32 !important;
    border: 1px solid #334155 !important;
    border-radius: 12px;
    padding: 18px;
}

[data-testid="stMetricLabel"] {
    color: #A8B5C7 !important;
}

[data-testid="stMetricValue"] {
    color: #F8FAFC !important;
}

.stTextArea textarea,
.stTextInput input {
    background-color: #111B2D !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
    border-radius: 9px !important;
}

.stTextArea textarea::placeholder,
.stTextInput input::placeholder {
    color: #94A3B8 !important;
    opacity: 1;
}

[data-testid="stFileUploader"] {
    background-color: #151F32 !important;
    border: 1px dashed #475569 !important;
    border-radius: 10px;
    padding: 12px;
}

[data-testid="stFileUploader"] * {
    color: #DCE5F1 !important;
}

.stButton > button {
    background-color: #1E293B;
    color: #F8FAFC !important;
    border: 1px solid #475569;
    border-radius: 8px;
    font-weight: 600;
    min-height: 42px;
}

.stButton > button:hover {
    background-color: #334155;
    border-color: #64748B;
}

.stButton > button[kind="primary"] {
    background-color: #D94350 !important;
    border: 1px solid #D94350 !important;
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: #B92E3B !important;
}

.stDownloadButton > button {
    width: 100%;
    background-color: #1E293B;
    color: #F8FAFC !important;
    border: 1px solid #475569;
    border-radius: 8px;
    min-height: 44px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid #334155;
}

.stTabs [data-baseweb="tab"] {
    color: #A8B5C7 !important;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: #F87171 !important;
    border-bottom-color: #F87171 !important;
}

[data-testid="stExpander"] {
    background-color: #151F32 !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

[data-testid="stExpander"] summary {
    color: #F1F5F9 !important;
}

[data-testid="stAlert"] {
    border-radius: 10px;
}

hr {
    border-color: #334155 !important;
}

[data-testid="stCodeBlock"] {
    border: 1px solid #334155;
    border-radius: 8px;
}

.severity-card {
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0 18px 0;
    border: 1px solid;
}

.severity-title {
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 8px;
}

.severity-description {
    font-size: 14px;
    margin-bottom: 6px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 6. HELPER FUNCTIONS
# =========================================================

def show_section(title):

    st.markdown(
        f'<div class="section-heading">{title}</div>',
        unsafe_allow_html=True
    )


def format_recommendation(recommendation):

    if isinstance(recommendation, dict):

        return {
            "priority": recommendation.get("priority", "Medium"),
            "action": recommendation.get("action", ""),
            "cause": recommendation.get("related_cause", "")
        }

    return {
        "priority": "Medium",
        "action": str(recommendation),
        "cause": ""
    }


def create_text_report(report, ai_result):

    services = report.get("affected_services", [])

    causes = report.get("likely_causes", [])

    recommendations = report.get("recommendations", [])

    ai_text = "Not available"

    if ai_result and ai_result.get("success"):
        ai_text = ai_result.get("analysis", "Not available")

    cause_text = "\n".join(
        item.get("cause", "Unknown")
        for item in causes
    )

    recommendation_text = "\n".join(
        f"[{item['priority']}] {item['action']}"
        for item in map(format_recommendation, recommendations)
    )

    return f"""
PAYGUARD AI
PAYMENT INCIDENT ANALYSIS REPORT
==========================================

Generated: {st.session_state.analysis_timestamp}

SEVERITY
------------------------------------------
{report.get("severity", "UNKNOWN")}

SEVERITY REASON
------------------------------------------
{report.get("severity_reason", "Not available")}

INCIDENT METRICS
------------------------------------------
Total Logs: {report.get("total_logs", 0)}
Total Events: {report.get("total_events", 0)}
Critical Events: {report.get("critical_events", 0)}
Errors: {report.get("errors", 0)}
Warnings: {report.get("warnings", 0)}

AFFECTED SERVICES
------------------------------------------
{chr(10).join(str(service) for service in services)}

LIKELY CAUSES
------------------------------------------
{cause_text}

RECOMMENDATIONS
------------------------------------------
{recommendation_text}

ESCALATION
------------------------------------------
{report.get("escalation", "Not available")}

GEMINI ANALYSIS
------------------------------------------
{ai_text}

==========================================
END OF REPORT
"""


# =========================================================
# 7. SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🛡️ PayGuard AI")

    st.caption("PAYMENT OPERATIONS INTELLIGENCE")

    st.divider()

    st.subheader("Navigation")

    st.markdown("📊 Incident Dashboard")
    st.markdown("📁 Log Analysis")
    st.markdown("🔍 Investigation")
    st.markdown("🤖 AI Intelligence")
    st.markdown("📄 Incident Reports")

    st.divider()

    st.subheader("AI Configuration")

    ai_available = is_ai_available()

    if ai_available:
        st.success("Gemini AI Connected")
    else:
        st.warning("Gemini AI Unavailable")

    enable_ai = st.checkbox(
        "Enable AI-assisted analysis",
        value=ai_available,
        disabled=not ai_available
    )

    st.divider()

    st.subheader("System Information")

    st.caption("Application: PayGuard AI")
    st.caption("Analysis: Rule-Based + Optional AI")
    st.caption("Framework: Streamlit")

    st.divider()

    st.caption("Version 1.2 | Prototype")


# =========================================================
# 8. HEADER
# =========================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        '<div class="main-heading">'
        'Incident Monitoring Dashboard'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="main-description">'
        'Monitor payment application logs, investigate incidents, '
        'and generate actionable troubleshooting insights.'
        '</div>',
        unsafe_allow_html=True
    )

with header_right:

    current_time = datetime.now()

    st.caption(current_time.strftime("%d %b %Y"))
    st.caption(current_time.strftime("%I:%M %p"))

st.divider()


# =========================================================
# 9. LOG INGESTION
# =========================================================

show_section("📂 Log Ingestion")

input_column, engine_column = st.columns([2.5, 1])

with input_column:

    uploaded_file = st.file_uploader(
        "Upload payment application logs",
        type=["txt", "log"],
        key=f"log_uploader_{st.session_state.upload_widget_version}"
    )

    if uploaded_file is not None:

        file_content = uploaded_file.getvalue()

        signature = hashlib.sha256(
            file_content
        ).hexdigest()

        if signature != st.session_state.last_uploaded_signature:

            try:

                uploaded_text = file_content.decode("utf-8")

                st.session_state.log_input = uploaded_text

                st.session_state.last_uploaded_signature = signature

                reset_analysis()

            except UnicodeDecodeError:

                st.error(
                    "Unable to read the uploaded file. "
                    "Please use UTF-8 encoded TXT or LOG files."
                )

    button1, button2 = st.columns(2)

    with button1:

        st.button(
            "📄 Load Sample Logs",
            on_click=load_sample_logs,
            use_container_width=True
        )

    with button2:

        st.button(
            "🗑️ Clear Logs",
            on_click=clear_logs,
            use_container_width=True
        )

    log_text = st.text_area(
        "Application Log Data",
        key="log_input",
        height=190,
        placeholder="Paste your payment application logs here...",
        on_change=reset_analysis
    )

    analyze_button = st.button(
        "🔍 Analyze Incident",
        type="primary",
        use_container_width=True
    )


# =========================================================
# 10. ANALYSIS ENGINE
# =========================================================

with engine_column:

    st.subheader("Analysis Engine")

    with st.container(border=True):

        st.markdown("**⚙️ Rule Engine**")

        st.caption(
            "Pattern matching and severity classification."
        )

        st.divider()

        st.markdown("**🔗 Correlation Engine**")

        st.caption(
            "Transaction and service-level event grouping."
        )

        st.divider()

        st.markdown("**🤖 Gemini AI**")

        st.caption(
            "Optional contextual analysis and investigation guidance."
        )

    st.info(
        "Suggested root causes are based on observed log patterns "
        "and require further investigation."
    )


# =========================================================
# 11. STATUS MESSAGES
# =========================================================

if st.session_state.success_message:

    st.success(st.session_state.success_message)

    st.session_state.success_message = None

if st.session_state.analysis_error:

    st.error(st.session_state.analysis_error)


# =========================================================
# 12. INCIDENT ANALYSIS
# =========================================================

if analyze_button:

    current_logs = st.session_state.log_input

    if not current_logs.strip():

        st.warning(
            "Please upload or paste application logs before analysis."
        )

    else:

        try:

            with st.spinner("Processing application logs..."):

                report = analyze_incident(current_logs)

            st.session_state.incident_report = report

            st.session_state.analysis_timestamp = datetime.now().strftime(
                "%d %b %Y, %I:%M:%S %p"
            )

            st.session_state.ai_result = None

            st.session_state.analysis_ai_enabled = enable_ai

            if enable_ai:

                with st.spinner("Gemini AI is analyzing the incident..."):

                    ai_result = analyze_with_ai(
                        current_logs,
                        incident_report=report
                    )

                st.session_state.ai_result = ai_result

            st.session_state.analysis_error = None

            st.success(
                "Incident analysis completed successfully."
            )

        except Exception as error:

            st.session_state.incident_report = None
            st.session_state.ai_result = None

            st.session_state.analysis_error = (
                f"Incident analysis failed: {type(error).__name__}"
            )

            print(
                f"Analysis error: {type(error).__name__}: {error}"
            )

            st.error(
                "Incident analysis failed. Please check the application logs."
            )


# =========================================================
# 13. INCIDENT RESULTS
# =========================================================

report = st.session_state.incident_report

if report:

    st.divider()

    show_section("📊 Incident Overview")

    severity = str(
        report.get("severity", "LOW")
    ).upper()

    severity_data = SEVERITY_CONFIG.get(
        severity,
        SEVERITY_CONFIG["LOW"]
    )

    severity_reason = report.get(
        "severity_reason",
        "No severity reason was provided by the rule engine."
    )

    st.markdown(
        f"""
        <div class="severity-card"
             style="
                background-color:{severity_data['background']};
                border-color:{severity_data['color']};
             ">

            <div class="severity-title"
                 style="color:{severity_data['color']};">
                {severity_data['icon']} {severity} SEVERITY
            </div>

            <div class="severity-description"
                 style="color:#F1F5F9;">
                {severity_data['description']}
            </div>

            <div class="severity-description"
                 style="color:#CBD5E1;">
                <b>Reason:</b> {severity_reason}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    metric_columns = st.columns(4)

    metrics = [
        ("Total Logs", report.get("total_logs", 0)),
        ("Total Events", report.get("total_events", 0)),
        ("Errors", report.get("errors", 0)),
        ("Warnings", report.get("warnings", 0))
    ]

    for column, (label, value) in zip(metric_columns, metrics):

        with column:
            st.metric(label, value)

    st.caption(
        f"Last analyzed: {st.session_state.analysis_timestamp}"
    )

    st.divider()

    show_section("🔍 Incident Investigation")

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Overview",
        "Root Cause & Evidence",
        "Timeline",
        "Correlation",
        "AI Analysis"
    ])

    # -----------------------------------------------------
    # TAB 1: OVERVIEW
    # -----------------------------------------------------

    with tab1:

        left, right = st.columns(2)

        with left:

            st.subheader("Affected Services")

            services = report.get("affected_services", [])

            if services:

                for service in services:
                    st.markdown(f"- 🟠 **{service}**")

            else:

                st.info("No affected services identified.")

        with right:

            st.subheader("Event Distribution")

            chart_data = pd.DataFrame({
                "Event Type": ["Errors", "Warnings"],
                "Count": [
                    report.get("errors", 0),
                    report.get("warnings", 0)
                ]
            })

            st.bar_chart(
                chart_data,
                x="Event Type",
                y="Count",
                color="#F87171"
            )

        st.divider()

        st.subheader("Troubleshooting Recommendations")

        recommendations = report.get("recommendations", [])

        if recommendations:

            for index, recommendation in enumerate(
                recommendations,
                start=1
            ):

                item = format_recommendation(recommendation)

                st.markdown(
                    f"**{index}. [{item['priority']} Priority]** "
                    f"{item['action']}"
                )

                if item["cause"]:
                    st.caption(f"Related cause: {item['cause']}")

        else:

            st.info("No recommendations generated.")

        st.divider()

        st.subheader("Escalation Guidance")

        st.info(
            report.get(
                "escalation",
                "No escalation guidance available."
            )
        )

    # -----------------------------------------------------
    # TAB 2: ROOT CAUSE AND EVIDENCE
    # -----------------------------------------------------

    with tab2:

        st.subheader("Likely Causes")

        st.caption(
            "Causes are inferred from matching log patterns. "
            "They are not confirmed root causes."
        )

        causes = report.get("likely_causes", [])

        if causes:

            for index, item in enumerate(causes, start=1):

                cause_name = item.get("cause", "Unknown cause")

                with st.expander(
                    f"{index}. {cause_name}",
                    expanded=True
                ):

                    if "confidence" in item:

                        st.write(
                            "**Confidence:**",
                            item["confidence"]
                        )

                    evidence_list = item.get("evidence", [])

                    if evidence_list:

                        for evidence in evidence_list:

                            st.write(
                                "**Line:**",
                                evidence.get("line_number", "N/A")
                            )

                            st.write(
                                "**Log Level:**",
                                evidence.get(
                                    "log_level",
                                    evidence.get("level", "N/A")
                                )
                            )

                            st.write(
                                "**Service:**",
                                evidence.get("service", "N/A")
                            )

                            st.code(
                                evidence.get("message", ""),
                                language="text"
                            )

                    else:

                        st.info("No supporting evidence found.")

        else:

            st.success("No likely causes were detected.")

        st.warning(
            "A matching log pattern does not prove the underlying root cause."
        )

    # -----------------------------------------------------
    # TAB 3: TIMELINE
    # -----------------------------------------------------

    with tab3:

        st.subheader("Incident Event Timeline")

        timeline = report.get("timeline", [])

        if timeline:

            for event in timeline:

                level = str(
                    event.get("level", "UNKNOWN")
                ).upper()

                icon = {
                    "CRITICAL": "🔴",
                    "FATAL": "🔴",
                    "ERROR": "🟠",
                    "WARNING": "🟡",
                    "WARN": "🟡",
                    "INFO": "🔵",
                    "DEBUG": "⚪"
                }.get(level, "⚪")

                st.markdown(
                    f"**{icon} {event.get('display_time', 'Unknown time')}**"
                )

                st.caption(
                    f"{level} | "
                    f"{event.get('service', 'Unknown service')}"
                )

                st.code(
                    event.get("message", ""),
                    language="text"
                )

        else:

            st.info("No timeline events available.")

    # -----------------------------------------------------
    # TAB 4: CORRELATION
    # -----------------------------------------------------

    with tab4:

        correlations = report.get("correlations", {})

        st.subheader("Payment / Transaction References")

        transaction_groups = correlations.get(
            "transaction_groups",
            {}
        )

        if transaction_groups:

            for reference, events in transaction_groups.items():

                with st.expander(
                    f"Reference {reference} | "
                    f"{len(events)} related events"
                ):

                    for event in events:

                        st.write(
                            f"Line {event.get('line_number', 'N/A')} | "
                            f"{event.get('level', 'UNKNOWN')} | "
                            f"{event.get('message', '')}"
                        )

        else:

            st.info(
                "No payment or transaction references detected."
            )

        st.divider()

        st.subheader("Service Correlation")

        service_groups = correlations.get(
            "service_groups",
            {}
        )

        if service_groups:

            service_counts = {
                service: len(events)
                for service, events in service_groups.items()
            }

            service_data = pd.DataFrame({
                "Service": list(service_counts.keys()),
                "Events": list(service_counts.values())
            })

            st.bar_chart(
                service_data,
                x="Service",
                y="Events",
                color="#60A5FA"
            )

            for service, events in service_groups.items():

                st.write(
                    f"**{service}:** {len(events)} related events"
                )

        else:

            st.info("No service correlations detected.")

        st.divider()

        st.subheader("Repeated Error Patterns")

        repeated_errors = correlations.get(
            "repeated_errors",
            {}
        )

        if repeated_errors:

            for pattern, events in repeated_errors.items():

                st.markdown(
                    f"- **{pattern}** — {len(events)} occurrences"
                )

        else:

            st.success("No repeated error patterns detected.")

        st.caption(
            "Correlation identifies related events. "
            "It does not independently establish causation."
        )

    # -----------------------------------------------------
    # TAB 5: AI ANALYSIS
    # -----------------------------------------------------

    with tab5:

        st.subheader("Gemini AI Intelligence")

        ai_result = st.session_state.ai_result

        if not st.session_state.analysis_ai_enabled:

            st.info(
                "AI-assisted analysis was not enabled for this incident. "
                "Rule-based findings remain available."
            )

        elif ai_result is None:

            st.info("No AI analysis is available.")

        elif ai_result.get("success"):

            st.success("Gemini analysis completed.")

            st.markdown(
                ai_result.get("analysis", "")
            )

            st.divider()

            st.subheader("Assessment Policy")

            st.info(
                "The rule-based severity is the primary application "
                "classification. Gemini provides an additional assessment "
                "for review."
            )

        else:

            st.error("Gemini analysis could not be completed.")

            st.warning(
                ai_result.get("error", "Unknown error.")
            )

            st.info(
                "Rule-based analysis is still available."
            )

    # -----------------------------------------------------
    # REPORT DOWNLOAD
    # -----------------------------------------------------

    st.divider()

    show_section("📄 Export Incident Report")

    ai_result = st.session_state.ai_result

    export_data = {
        "application": "PayGuard AI",
        "generated_at": st.session_state.analysis_timestamp,
        "rule_based_report": report,
        "gemini_analysis": ai_result
    }

    json_report = json.dumps(
        export_data,
        indent=4,
        default=str
    )

    text_report = create_text_report(
        report,
        ai_result
    )

    download1, download2 = st.columns(2)

    with download1:

        st.download_button(
            "⬇️ Download JSON Report",
            data=json_report,
            file_name="payguard_incident_report.json",
            mime="application/json",
            use_container_width=True
        )

    with download2:

        st.download_button(
            "⬇️ Download Text Report",
            data=text_report,
            file_name="payguard_incident_report.txt",
            mime="text/plain",
            use_container_width=True
        )


# =========================================================
# 14. EMPTY DASHBOARD
# =========================================================

else:

    st.divider()

    st.title("🛡️ Welcome to PayGuard AI")

    st.markdown(
        "Your payment incident investigation workspace."
    )

    st.caption(
        "Upload application logs or load sample data to begin."
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Rule Engine", "Ready")

    with col2:
        st.metric(
            "Gemini AI",
            "Connected" if is_ai_available() else "Offline"
        )

    with col3:
        st.metric("Incident Status", "Awaiting Logs")

    st.info(
        "Start by clicking Load Sample Logs or uploading a TXT/LOG file."
    )


# =========================================================
# 15. FOOTER
# =========================================================

st.divider()

st.caption("PayGuard AI | Intelligent Payment Incident Analyzer")
st.caption("Rule-Based Analysis with Gemini Assistance")
st.caption("All findings should be reviewed before taking action.")