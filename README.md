🛡️ PayGuard AI

Intelligent Payment Incident Analyzer

Python | Streamlit | Google Gemini API | Log Analysis | Incident Management

An AI-assisted application that analyzes payment application logs, identifies potential failures, classifies incident severity, correlates related events, and provides troubleshooting recommendations.

GitHub Repository: https://github.com/Kartik2473/PayGuard-AI

⸻

📌 1. Project Overview

PayGuard AI is a Python-based incident analysis application designed to help Technology Operations and application support teams investigate payment application failures using application logs.

In distributed payment applications, failures can occur across different services, making it difficult to identify the source of an incident and determine the appropriate troubleshooting steps.

PayGuard AI addresses this problem by combining rule-based log analysis, event correlation, and optional generative AI assistance.

The application processes payment-related logs and provides structured incident information, including:

* Error and warning detection.
* Incident severity classification.
* Potential root cause identification.
* Supporting evidence from original log entries.
* Affected service identification.
* Transaction and event correlation.
* Troubleshooting recommendations.
* Escalation guidance.
* AI-assisted incident investigation.
* Downloadable JSON and TXT reports.

The application uses a hybrid architecture in which the core rule-based analysis engine operates independently of the external Gemini API.

Project Information

Field	Details
Project	PayGuard AI
Project Type	Software Engineering and AI Integration
Domain	Payment Technology Operations
Development	Individual Project
Backend	Python
Frontend	Streamlit
AI Integration	Google Gemini API

⸻

🎯 2. Problem Statement

Payment applications generate large volumes of logs containing information about transactions, service failures, API errors, database connectivity, authentication problems, and other operational events.

Manually investigating these logs can be time-consuming, particularly when multiple errors occur across different services.

An operations engineer needs to answer:

1. What went wrong?
2. Which services were affected?
3. How severe is the incident?
4. What evidence supports the suspected cause?
5. Which issue should be investigated first?
6. What troubleshooting steps should be performed?
7. When should the incident be escalated?

PayGuard AI provides a structured approach to answering these questions through automated log analysis and optional AI-assisted investigation.

⸻

🚀 3. Key Features

3.1 Log Ingestion

* Upload TXT and LOG files.
* Paste application logs manually.
* Load sample payment logs.
* Clear existing logs and analysis.

3.2 Automated Log Processing

* Parse individual log entries.
* Identify log levels.
* Extract timestamps and service information.
* Count errors, warnings, and critical events.
* Identify relevant failure messages.

3.3 Incident Severity Classification

The rule-based engine classifies incidents into four severity levels.

Severity	Description
🔴 CRITICAL	Immediate investigation required
🟠 HIGH	Urgent investigation recommended
🟡 MEDIUM	Investigation and monitoring required
🟢 LOW	Continue normal monitoring

Severity is determined using predefined Python rules and detected log patterns.

3.4 Potential Root Cause Identification

Identifies possible failure patterns, including:

* API timeouts.
* Database connection failures.
* Authentication failures.
* Service unavailability.
* Payment declines and insufficient funds.

These are potential causes based on available log evidence, not automatically confirmed root causes.

3.5 Evidence Traceability

Provides supporting information from original log entries:

* Line numbers.
* Log levels.
* Service names.
* Original log messages.

This helps an engineer verify why a particular failure pattern was identified.

3.6 Event Correlation

The correlation engine:

* Extracts payment and transaction references.
* Groups related transaction events.
* Groups events by service.
* Identifies repeated error patterns.
* Generates an incident timeline.

3.7 Troubleshooting and Escalation

Provides investigation recommendations and escalation guidance based on detected failure patterns and incident severity.

3.8 Google Gemini AI Integration

Integrates Google’s Gemini API to provide optional contextual incident analysis.

The AI component can assist with:

* Understanding failure patterns.
* Reviewing incident context.
* Suggesting possible causes.
* Recommending additional investigation steps.

AI-generated findings are displayed separately from rule-based results and require human verification.

3.9 Incident Report Export

Supports downloading incident analysis in:

* JSON format.
* TXT format.

Reports include incident information, severity, metrics, potential causes, recommendations, escalation guidance, and available AI analysis.

3.10 Independent Rule-Based Fallback

The core incident analysis functionality does not depend on Gemini.

If the API is unavailable or not configured, the application can still process logs and generate rule-based findings.

⸻

🛠️ 4. Technology Stack

Technology	Purpose
Python	Core application logic
Streamlit	Interactive dashboard
Google Gemini API	AI-assisted incident analysis
Google GenAI SDK	Gemini API integration
Pandas	Data handling and visualization
Regular Expressions	Log parsing and pattern detection
Python unittest	Automated testing
python-dotenv	Environment variable management
Git and GitHub	Version control and project management

⸻

🏗️ 5. System Architecture

PayGuard AI follows a modular architecture that separates log processing, incident analysis, correlation, AI integration, and dashboard functionality.

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
                +-------+-------+
                |               |
                v               v
          Severity Engine   Correlation Engine
                |               |
                +-------+-------+
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
                JSON / TXT Export

Main Application Components

Component	File	Responsibility
Streamlit Dashboard	app.py	User interface, analysis workflow and report downloads
AI Engine	ai_engine.py	Gemini API integration
Incident Analyzer	incident_analyzer.py	Potential causes, evidence, recommendations and escalation
Log Processor	log_processor.py	Log parsing, timestamps, levels and service extraction
Correlation Engine	correlation_engine.py	Transaction correlation, repeated errors and timelines
Severity Classification	log_processor.py	Rule-based incident severity classification

⸻

📂 6. Project Structure

The project follows a modular directory structure, separating application logic, AI integration, log processing, testing, screenshots, and configuration.

PayGuard-AI/
│
├── app.py                         # Streamlit application and dashboard
├── ai_engine.py                   # Google Gemini API integration
├── incident_analyzer.py           # Incident analysis and recommendations
├── log_processor.py               # Log parsing and severity classification
├── correlation_engine.py          # Transaction and event correlation
│
├── requirements.txt               # Python dependencies
├── README.md                      # Project documentation
├── .gitignore                     # Excludes sensitive and unnecessary files
├── .env.example                   # Environment variable template
│
├── screenshots/
│   ├── dashboard.png              # Incident monitoring dashboard
│   └── welcome.png                # Application welcome dashboard
│
├── sample_logs/
│   └── payment_logs.txt           # Sample payment application logs
│
├── tests/
│   └── test_incident_analyzer.py  # Automated unit tests
│
└── PineLabs_Incident_Analyzer/
    └── .streamlit/
        └── config.toml            # Streamlit configuration

File Responsibilities

File / Directory	Responsibility
app.py	Streamlit dashboard and application workflow
ai_engine.py	Gemini API integration
incident_analyzer.py	Incident analysis and recommendations
log_processor.py	Log parsing and severity classification
correlation_engine.py	Transaction and event correlation
screenshots/	Application screenshots
sample_logs/	Sample payment application logs
tests/	Automated unit tests
requirements.txt	Python dependencies
.env.example	Environment configuration template
.gitignore	Excludes sensitive and unnecessary files
.streamlit/config.toml	Streamlit configuration

🔐 Security

The actual .env file, API credentials, and Python virtual environment are local development files.

They must never be committed to the public GitHub repository or included in the submission ZIP.

The .env.example file contains placeholder configuration values only.

⸻

🖥️ 7. Application Screenshots

PayGuard AI provides an interactive Streamlit dashboard for payment incident investigation, log analysis, AI-assisted troubleshooting, and incident reporting.

7.1 Incident Monitoring Dashboard

The main dashboard provides log ingestion, sample log loading, incident analysis, and access to the rule-based and AI analysis engines.

7.2 Application Welcome Dashboard

The welcome section displays the application status, rule engine availability, Gemini AI connection status, and incident monitoring workspace.

⸻

⚙️ 8. Installation and Setup

Prerequisites

* Python 3.10 or later.
* pip package manager.
* Git.
* Internet connection for optional Gemini API integration.

Step 1: Clone the Repository

git clone https://github.com/Kartik2473/PayGuard-AI.git

Navigate to the project directory:

cd PayGuard-AI

Step 2: Create a Virtual Environment

macOS/Linux

python3 -m venv venv

Windows

python -m venv venv

Step 3: Activate the Environment

macOS/Linux

source venv/bin/activate

Windows

venv\Scripts\activate

Step 4: Install Dependencies

pip install -r requirements.txt

⸻

🤖 9. Gemini API Configuration

PayGuard AI supports optional Gemini AI integration.

Create a .env file in the project root directory.

Add the following configuration:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite

Replace the placeholder with your own Gemini API key.

Important: Never commit your actual API key to GitHub or share it in screenshots, documentation, or public repositories.

If Gemini is not configured or unavailable, rule-based incident analysis remains available.

⸻

▶️ 10. Running the Application

Start the Streamlit application:

streamlit run app.py

Open the application in your browser.

Local URL:

http://localhost:8501

The application runs locally on your machine. The URL is accessible from the machine running Streamlit.

Application Workflow

1. Open the PayGuard AI dashboard.
2. Upload a TXT or LOG file, or paste application logs.
3. Enable optional Gemini AI analysis if required.
4. Click Analyze Incident.
5. Review incident severity and metrics.
6. Examine potential causes and supporting evidence.
7. Review the event timeline and transaction correlations.
8. Review optional Gemini AI analysis.
9. Download the JSON or TXT incident report.

⸻

🧪 11. Sample Input

The following payment logs can be used to test the application.

2026-11-18 10:00:01 INFO Payment service started
2026-11-18 10:00:05 INFO Processing payment ID 1001
2026-11-18 10:00:08 ERROR Payment API timeout
2026-11-18 10:00:10 ERROR Database connection failed
2026-11-18 10:00:12 CRITICAL Payment service unavailable
2026-11-18 10:00:15 WARNING Retry limit approaching
2026-11-18 10:00:20 INFO Monitoring system active

The application processes these entries to identify potential failures, classify severity, extract supporting evidence, and recommend investigation steps.

⸻

✅ 12. Testing

The project includes automated tests using Python’s unittest framework.

Run the test suite:

python3 -m unittest discover -s tests -v

Test Coverage

The current test suite contains 11 test cases covering:

* Basic log processing.
* Empty log handling.
* Unknown text and error-level detection.
* Critical severity classification.
* High severity classification.
* Medium severity classification.
* Low severity classification.
* Authentication failure detection.
* Incident report structure.
* Evidence traceability.

Test Results

Development test run: 11 tests passed.

Gemini API integration was also tested separately. The automated unit tests primarily validate the rule-based components.

⸻

💡 13. Skills Demonstrated

This project demonstrates practical experience in the following areas.

Programming and Development

* Python programming.
* Modular application development.
* Functions and data structures.
* Regular expressions.
* Exception handling.
* Environment variable management.

Backend and Data Processing

* Text and log processing.
* Data extraction and transformation.
* Pattern matching.
* Event correlation.
* JSON report generation.

Software Engineering

* Modular architecture.
* Separation of responsibilities.
* Version control using Git.
* Dependency management.
* Automated unit testing.
* Debugging and application testing.

Artificial Intelligence

* External AI API integration.
* Prompt-based contextual analysis.
* AI-assisted troubleshooting.
* Rule-based and AI-based analysis.
* Human verification of AI-generated results.

Technology Operations

* Application log investigation.
* Error identification.
* Incident severity classification.
* Evidence-based troubleshooting.
* Escalation guidance.
* Incident reporting.

⸻

📚 14. Learning Outcomes

Through this project, I gained practical experience in:

1. Building a modular Python application.
2. Processing and analyzing application logs.
3. Designing rule-based classification logic.
4. Identifying potential application failure patterns.
5. Correlating related events using transaction references.
6. Integrating an external generative AI API.
7. Developing an interactive dashboard using Streamlit.
8. Implementing automated tests using Python unittest.
9. Managing project dependencies and environment variables.
10. Using Git and GitHub for source-code management.

These concepts are relevant to software development, backend engineering, application support, technology operations, and AI-assisted automation.

⸻

⚠️ 15. Assumptions and Limitations

Assumptions

* Input logs are provided as text.
* Log formats may vary between applications.
* Some log entries may not contain timestamps or service names.
* Severity classification uses predefined rules.
* Transaction correlation depends on identifiable payment references.
* Recommendations require validation by support engineers.

Limitations

* Root cause identification depends on available log evidence and predefined patterns.
* Missing timestamps can affect timeline accuracy.
* Missing transaction identifiers limit event correlation.
* Gemini may generate incorrect or unsupported hypotheses.
* AI analysis depends on API availability and usage quotas.
* The application does not connect to live payment infrastructure.
* The application does not automatically execute remediation actions.
* Severity classification is rule-based and does not independently measure actual business impact.

⸻

🔮 16. Future Improvements

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

⸻

🎓 17. Career and Technical Relevance

PayGuard AI is a practical project demonstrating concepts that are useful across several technical career paths.

Career Area	Relevant Project Concepts
Python Developer	Python programming, modular development and data processing
Backend Developer	Application logic, API integration and JSON processing
Java Developer	Incident analysis concepts, service failures and backend troubleshooting
Data Engineer	Log processing, data extraction and transformation
Technical Support Engineer	Error investigation, evidence analysis and troubleshooting
Technology Operations	Incident classification, escalation and reporting
AI Application Developer	Gemini API integration and AI-assisted analysis

The project can also support technical preparation for CDAC by providing practical exposure to programming, data structures and problem-solving, software architecture, API integration, and testing concepts.

⸻

👨‍💻 18. Author

Kartik Mathpati

B.Tech – Computer Engineering

Connect

* GitHub Profile: Kartik2473
* Project Repository: PayGuard AI

⸻

📌 Final Note

PayGuard AI demonstrates how Python-based log processing, rule-based incident classification, event correlation, and generative AI can be combined to support payment technology operations.

The project focuses on building a practical incident investigation tool that helps engineers understand application failures, review supporting evidence, identify potential causes, and prioritize troubleshooting activities.

It is a prototype intended for learning, demonstration, and further development. It is not a production payment monitoring or automated remediation platform.