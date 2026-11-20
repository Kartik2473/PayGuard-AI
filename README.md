PayGuard AI

Intelligent Payment Incident Analyzer

Technology Operations Intern – Practical AI Assignment

Project Information	Details
Project	PayGuard AI
Candidate	Kartik Mathpati
Domain	Payment Technology Operations
Application	AI-Assisted Incident Analysis System
Backend	Python
Frontend	Streamlit
AI Integration	Google Gemini API

⸻

1. Project Overview

PayGuard AI is an AI-assisted payment incident analysis application designed to help Technology Operations teams investigate application failures using application logs.

The application processes payment-related logs, identifies errors and repeated failure patterns, classifies incident severity, identifies affected services, and generates troubleshooting recommendations.

It combines custom Python-based log processing, rule-based incident analysis, event correlation, and Google’s Gemini generative AI model.

The application supports independent rule-based analysis, allowing core functionality to remain available even when the external AI service is unavailable.

2. Problem Statement

Payment applications generate large volumes of application logs. When failures occur across multiple services, manually identifying the underlying problems can be time-consuming.

Technology Operations engineers need to understand:

* What went wrong?
* Which services were affected?
* How serious is the incident?
* What evidence supports the suspected cause?
* What should be investigated first?
* When should the issue be escalated?

PayGuard AI addresses these requirements through automated log analysis and optional AI-assisted investigation.

3. Project Objectives

1. Automate payment application log analysis.
2. Identify errors, warnings, and critical events.
3. Classify incidents into Critical, High, Medium, and Low severity.
4. Identify potential causes using predefined log patterns.
5. Display supporting evidence from original log entries.
6. Correlate events using payment and transaction references.
7. Generate practical troubleshooting recommendations.
8. Integrate generative AI for contextual incident analysis.
9. Generate structured incident reports.
10. Provide an interactive dashboard for incident investigation.

4. Key Features

Log Ingestion

* Upload TXT and LOG files.
* Paste application logs manually.
* Load sample payment logs.
* Clear existing logs and analysis.

Automated Log Analysis

* Process application log entries.
* Identify log levels.
* Count errors and warnings.
* Extract timestamps and service information.

Severity Classification

The rule-based engine classifies incidents into four categories:

Severity	Description
CRITICAL	Immediate investigation required
HIGH	Urgent investigation recommended
MEDIUM	Investigation and monitoring required
LOW	Continue normal monitoring

Severity is determined using predefined Python rules and detected log patterns.

Potential Root Cause Identification

Identifies possible failure patterns, including:

* API timeouts.
* Database connection failures.
* Authentication failures.
* Service unavailability.
* Payment declines and insufficient funds.

Evidence Traceability

Displays supporting information from original logs, including:

* Line numbers.
* Log levels.
* Service names.
* Original log messages.

Potential causes are distinguished from confirmed findings.

Event Correlation

The correlation engine:

* Extracts payment and transaction references.
* Groups related transaction events.
* Groups events by service.
* Identifies repeated error patterns.
* Generates an incident timeline.

Troubleshooting and Escalation

Provides suggested investigation steps and escalation guidance based on detected incident patterns and severity.

Gemini AI Integration

Uses Google’s Gemini API to provide optional contextual incident analysis and investigation recommendations.

AI-generated findings are presented separately from rule-based results and require human verification.

Incident Report Export

Supports exporting incident analysis in:

* JSON format.
* TXT format.

Reports include incident information, severity, metrics, potential causes, recommendations, escalation guidance, and available AI analysis.

Fallback Mechanism

The rule-based analysis engine operates independently of Gemini. If the external AI service is unavailable, the application can still process logs and generate rule-based findings.

5. Technology Stack

Technology	Purpose
Python	Core application logic
Streamlit	Interactive dashboard
Google Gemini	AI-assisted incident analysis
Google GenAI SDK	Gemini API integration
Pandas	Data handling and visualization
Regular Expressions	Log parsing and pattern detection
Python unittest	Automated testing
python-dotenv	Environment variable management

6. System Architecture

The application follows a modular architecture.

Processing Workflow

       Application Logs
              |
              v
     Log Input (Upload/Paste)
              |
              v
        Log Processor
              |
              v
      Rule-Based Analysis
              |
       +------+------+
       |             |
       v             v
 Severity Engine  Correlation Engine
       |             |
       +------+------+
              |
              v
      Incident Report
              |
              v
      Optional Gemini AI
              |
              v
     Incident Investigation
              |
              v
    Streamlit Dashboard
              |
              v
   JSON / TXT Report Export

Main Components

1. Log Processor (log_processor.py)

Responsible for reading application log entries, extracting timestamps, identifying log levels, detecting service information, and counting errors and warnings.

2. Severity Classification Engine

Uses predefined Python rules to classify incidents into Critical, High, Medium, and Low categories.

3. Incident Analyzer (incident_analyzer.py)

Identifies potential failure patterns, extracts supporting evidence, identifies affected services, generates troubleshooting recommendations, and provides escalation guidance.

4. Correlation Engine (correlation_engine.py)

Extracts payment references, groups related events, identifies repeated errors, and generates incident timelines.

5. AI Engine (ai_engine.py)

Integrates Google’s Gemini API to provide contextual incident analysis and additional investigation guidance.

6. Streamlit Dashboard (app.py)

Provides the interactive interface for log ingestion, incident analysis, evidence review, correlation, AI analysis, and report downloads.

7. Project Structure

PineLabs_Incident_Analyzer/
│
├── app.py
├── ai_engine.py
├── incident_analyzer.py
├── log_processor.py
├── correlation_engine.py
│
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
│
├── sample_logs/
│   └── payment_logs.txt
│
└── tests/
    └── test_incident_analyzer.py

The .env file and virtual environment are local development files and must not be committed to the public repository or included in the submission ZIP.

8. Installation and Setup

Prerequisites

* Python 3.10 or later.
* pip package manager.
* Internet connection for optional Gemini API integration.

Step 1: Clone the Repository

git clone YOUR_GITHUB_REPOSITORY_URL

Navigate into the project:

cd PineLabs_Incident_Analyzer

Alternatively, extract the downloaded project ZIP.

Step 2: Create a Virtual Environment

macOS/Linux:

python3 -m venv venv

Windows:

python -m venv venv

Step 3: Activate the Environment

macOS/Linux:

source venv/bin/activate

Windows:

venv\Scripts\activate

Step 4: Install Dependencies

pip install -r requirements.txt

9. Gemini API Configuration

PayGuard AI supports optional Gemini AI integration.

Create a .env file in the project root:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite

Replace the placeholder with your own Gemini API key.

Never commit your actual API key to GitHub or share it in screenshots or documentation.

If Gemini is not configured or unavailable, rule-based incident analysis remains available.

10. Running the Application

Start the Streamlit application:

streamlit run app.py

Open the following address in your browser:

http://localhost:8501

Application Workflow

1. Open the PayGuard AI dashboard.
2. Upload a TXT or LOG file, or paste application logs.
3. Enable optional Gemini AI analysis if required.
4. Click Analyze Incident.
5. Review the severity classification and incident metrics.
6. Examine potential causes and supporting evidence.
7. Review the event timeline and transaction correlations.
8. Review optional Gemini AI analysis.
9. Download the JSON or TXT incident report.

11. Sample Input

2026-11-18 10:00:01 INFO Payment service started
2026-11-18 10:00:05 INFO Processing payment ID 1001
2026-11-18 10:00:08 ERROR Payment API timeout
2026-11-18 10:00:10 ERROR Database connection failed
2026-11-18 10:00:12 CRITICAL Payment service unavailable
2026-11-18 10:00:15 WARNING Retry limit approaching
2026-11-18 10:00:20 INFO Monitoring system active

The application processes these entries to identify potential failures, classify severity, extract evidence, and recommend investigation steps.

12. Automated Testing

The project includes automated tests using Python’s unittest framework.

Run the tests:

python3 -m unittest discover -s tests -v

The current test suite contains 11 test cases covering:

* Basic log processing.
* Empty log handling.
* Malformed-line handling and error-level detection.
* Critical severity classification.
* High severity classification.
* Medium severity classification.
* Low severity classification.
* Authentication failure detection.
* Incident report structure.
* Evidence traceability.

The development test run passed all 11 tests.

Gemini API integration was also tested separately. The automated unit tests primarily validate the rule-based components.

13. Assumptions

* Input logs are provided as text.
* Log formats may vary between applications.
* Some log entries may not contain timestamps or service names.
* Severity classification uses predefined rules.
* AI-generated root causes are hypotheses, not confirmed findings.
* Transaction correlation depends on identifiable payment references.
* Recommendations require validation by support engineers.

14. Limitations

* Root cause identification depends on available log evidence and predefined patterns.
* Missing timestamps can affect timeline accuracy.
* Missing transaction identifiers limit event correlation.
* Gemini may generate incorrect or unsupported hypotheses.
* AI analysis depends on API availability and usage quotas.
* The application does not connect to live payment infrastructure.
* The application does not automatically execute remediation actions.
* Severity classification is rule-based and does not independently measure actual business impact.

15. Future Improvements

Potential enhancements include:

* Support for additional log formats.
* Advanced anomaly detection.
* Improved service dependency mapping.
* Historical incident analysis.
* Integration with monitoring platforms.
* Advanced transaction correlation.
* Role-based access control.
* Integration with ITSM platforms.
* Automated incident workflow management.

16. Conclusion

PayGuard AI demonstrates how Python-based log processing, rule-based incident classification, event correlation, and generative AI can be combined to support payment technology operations.

The application provides a structured approach to incident investigation, helping support engineers understand application failures, review supporting evidence, identify potential causes, and prioritize troubleshooting activities.

Its hybrid architecture ensures that core incident analysis remains available independently of the external AI service.

⸻

Project: PayGuard AI – Intelligent Payment Incident Analyzer
Developed by: Kartik Mathpati
Assignment: Technology Operations Intern – Practical AI Assignment
Domain: AI, Python, Payment Operations, Incident Management