🛡️ PayGuard AI

Intelligent AI-Assisted Application Incident Analyzer

Python | Streamlit | Google Gemini API | Log Analysis | Incident Management | Troubleshooting

PayGuard AI is an AI-assisted application incident analysis platform designed to help developers, application support engineers, and Technology Operations teams investigate software failures through automated log analysis.

The application processes application logs, identifies potential failures, classifies incident severity, correlates related events, identifies possible root causes, and generates troubleshooting recommendations.

It combines rule-based analysis with optional Generative AI capabilities to simplify incident investigation and improve operational visibility.

Designed for: Payment Systems | Banking | FinTech | E-commerce | Enterprise Applications | Backend Services | Distributed Systems
---

## 📌 1. Project Overview

Modern software applications generate large volumes of logs across different services, databases, APIs, and infrastructure components.

Identifying the source of an application failure can be challenging, particularly when multiple services are involved.

PayGuard AI addresses this challenge by combining rule-based log analysis, event correlation, and optional Generative AI assistance.

The application provides structured incident information, including:

* Automated error and warning detection.
* Incident severity classification.
* Potential root cause identification.
* Supporting evidence from original log entries.
* Affected service identification.
* Transaction and event correlation.
* Troubleshooting recommendations.
* Escalation guidance.
* AI-assisted incident investigation.
* Downloadable JSON and TXT reports.

The application follows a hybrid architecture in which the core rule-based analysis engine operates independently of the external Gemini API.

Project Information

Field	Details
Project	PayGuard AI
Project Type	Software Engineering and AI Integration
Domain	Application Incident Management
Development	Individual Project
Backend	Python
Frontend	Streamlit
AI Integration	Google Gemini API
Analysis	Rule-Based and AI-Assisted
Reporting	JSON and TXT

---

## 🎯 2. Problem Statement

Software applications frequently encounter operational issues, including API failures, database connectivity problems, authentication errors, service interruptions, and unexpected application exceptions.

Manually investigating these problems can be time-consuming, particularly when multiple errors occur across different services.

Technology Operations engineers need to answer:

1. What went wrong?
2. Which services or components were affected?
3. How severe is the incident?
4. What evidence supports the suspected cause?
5. Which issue should be investigated first?
6. What troubleshooting steps should be performed?
7. When should the incident be escalated?

PayGuard AI provides a structured approach to answering these questions through automated log processing, rule-based analysis, event correlation, and optional AI-assisted investigation.

---

## 🚀 3. Key Features

3.1 Log Ingestion

* Upload TXT and LOG files.
* Paste application logs manually.
* Load sample application logs.
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
* Payment declines.
* Insufficient funds.
* Application errors.

These findings represent potential causes based on available log evidence and predefined detection patterns, not automatically confirmed root causes.

3.5 Evidence Traceability

Provides supporting information from original log entries:

* Line numbers.
* Log levels.
* Service names.
* Original log messages.
* Relevant failure events.

This helps engineers verify why a particular failure pattern was identified.

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
* Suggesting potential root causes.
* Recommending additional investigation steps.
* Generating contextual troubleshooting guidance.

AI-generated findings are displayed separately from rule-based results and require human verification.

3.9 Incident Report Export

Supports downloading incident analysis in:

* JSON format.
* TXT format.

Reports include incident information, severity, metrics, potential causes, recommendations, escalation guidance, and available AI analysis.

3.10 Independent Rule-Based Fallback

The core incident analysis functionality does not depend on Gemini.

If the API is unavailable or not configured, the application can still process logs and generate rule-based findings.

---

## 🛠️ 4. Technology Stack

Technology	Purpose
Python	Core application logic
Streamlit	Interactive dashboard
Google Gemini API	AI-assisted incident analysis
Google GenAI SDK	Gemini API integration
Pandas	Data handling and processing
Regular Expressions	Log parsing and pattern detection
Python unittest	Automated testing
python-dotenv	Environment variable management
Git and GitHub	Version control and project management

---

## 🏗️ 5. System Architecture

PayGuard AI follows a modular architecture that separates log processing, incident analysis, event correlation, AI integration, and dashboard functionality.

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
                 Incident Analyzer
                        |
                        v
                 Incident Report
                        |
                        v
                Optional Gemini AI
                        |
                        v
             AI-Assisted Investigation
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

---

## 📂 6. Project Structure

The project follows a modular directory structure, separating application logic, AI integration, log processing, testing, screenshots, configuration, and documentation.

### Directory Structure

```text
PayGuard-AI/
│
├── PineLabs_Incident_Analyzer/
│   └── .streamlit/
│       └── config.toml
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
├── screenshots/
│   ├── dashboard.png
│   └── welcome.png
│
├── sample_logs/
│   └── payment_logs.txt
│
└── tests/
    └── test_incident_analyzer.py
```

### File Responsibilities

| File / Directory | Responsibility |
|---|---|
| `app.py` | Main Streamlit dashboard and application workflow |
| `ai_engine.py` | Google Gemini API integration |
| `incident_analyzer.py` | Incident analysis, potential causes and troubleshooting recommendations |
| `log_processor.py` | Log parsing, timestamp extraction and severity classification |
| `correlation_engine.py` | Transaction correlation and event timelines |
| `screenshots/` | Application screenshots |
| `sample_logs/` | Sample payment application logs |
| `tests/` | Automated unit tests |
| `requirements.txt` | Python project dependencies |
| `README.md` | Project documentation |
| `.env.example` | Environment variable configuration template |
| `.gitignore` | Excludes sensitive and unnecessary files |
| `PineLabs_Incident_Analyzer/.streamlit/config.toml` | Streamlit application configuration |
---

## 🔐 7. Security

The application follows basic security and configuration management practices.

* The actual .env file is maintained locally.
* API credentials are stored using environment variables.
* .env.example contains placeholder configuration values only.
* .gitignore excludes sensitive and unnecessary development files.
* API credentials must never be committed to GitHub.
* API keys must not be exposed in screenshots, documentation, or public repositories.
* Python virtual environments should not be included in the submission ZIP.

The application uses optional external AI integration. Core rule-based functionality remains available when the Gemini API is unavailable.

---

## 🖥️ 8. Application Screenshots

PayGuard AI provides an interactive Streamlit dashboard for application incident investigation, log analysis, AI-assisted troubleshooting, and incident reporting.

8.1 Incident Monitoring Dashboard

The main dashboard provides log ingestion, sample log loading, incident analysis, severity classification, and access to the rule-based and AI analysis engines.

8.2 Application Welcome Dashboard

The welcome section displays application status, rule engine availability, Gemini AI connection status, and the incident monitoring workspace.

---

## ⚙️ 9. Installation and Setup

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

macOS / Linux

python3 -m venv venv

Windows

python -m venv venv

Step 3: Activate the Environment

macOS / Linux

source venv/bin/activate

Windows

venv\Scripts\activate

Step 4: Install Dependencies

pip install -r requirements.txt

---

## 🤖 10. Gemini API Configuration

PayGuard AI supports optional Google Gemini API integration.

Create a .env file in the project root directory and add:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-3.5-flash-lite

Replace the placeholder with your Gemini API key.

Security Notes:

* Never upload your API key to GitHub.
* Keep .env in .gitignore.
* Use .env.example for sample configuration.

If Gemini is unavailable, rule-based incident analysis continues to work.

---

## ▶️ 11. Running the Application

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

---

## 🧪 12. Sample Input

The following sample payment application logs can be used to test PayGuard AI's log processing, incident detection, severity classification, and troubleshooting capabilities.

### Sample Payment Application Logs

```text
2026-11-18 10:00:01 INFO Payment service started
2026-11-18 10:00:05 INFO Processing payment ID 1001
2026-11-18 10:00:08 ERROR Payment API timeout
2026-11-18 10:00:10 ERROR Database connection failed
2026-11-18 10:00:12 CRITICAL Payment service unavailable
2026-11-18 10:00:15 WARNING Retry limit approaching
2026-11-18 10:00:20 INFO Monitoring system active
```

### Expected Analysis

The application processes the supplied logs to identify potential failures and generate structured incident information.

| Log Entry | Detected Information |
|---|---|
| Payment service started | Service initialization |
| Processing payment ID 1001 | Payment transaction activity |
| Payment API timeout | API communication failure |
| Database connection failed | Database connectivity issue |
| Payment service unavailable | Critical service failure |
| Retry limit approaching | Potential retry exhaustion |
| Monitoring system active | Monitoring activity |

### Analysis Output

PayGuard AI uses the supplied log entries to:

- Identify errors, warnings, and critical events.
- Classify incident severity using predefined rules.
- Identify potential failure patterns.
- Extract supporting evidence from original logs.
- Correlate related transaction and service events.
- Generate troubleshooting recommendations.
- Provide optional Gemini AI-assisted analysis.
- Generate downloadable JSON and TXT incident reports.

**Note:** The analysis results depend on the application's implemented detection rules and available log evidence. Potential root causes require verification by an engineer.
---

## ✅ 13. Testing

The project includes automated tests using Python’s unittest framework.

Run the Test Suite

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

Development Test Run: 11 Tests Passed.

Gemini API integration was also tested separately. The automated unit tests primarily validate the rule-based components.

---

## 💡 14. Skills Demonstrated

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

---

## 📚 15. Learning Outcomes

Through this project, I gained practical experience in:

1. Building a modular Python application.
2. Processing and analyzing application logs.
3. Designing rule-based classification logic.
4. Identifying potential application failure patterns.
5. Correlating related events using transaction references.
6. Integrating an external Generative AI API.
7. Developing an interactive dashboard using Streamlit.
8. Implementing automated tests using Python unittest.
9. Managing project dependencies and environment variables.
10. Using Git and GitHub for source-code management.

These concepts are relevant to software development, backend engineering, application support, technology operations, and AI-assisted automation.

---

## ⚠️ 16. Assumptions and Limitations

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
* The application does not connect to live production infrastructure.
* The application does not automatically execute remediation actions.
* Severity classification is rule-based and does not independently measure actual business impact.
* Additional parsing and detection rules are required to support different application domains.

---

## 🔮 17. Future Improvements

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
* Real-time log ingestion.
* Domain-specific incident detection.

---

## 🎓 18. Career and Technical Relevance

PayGuard AI demonstrates practical concepts relevant to several technical career paths.

Career Area	Relevant Project Concepts
Python Developer	Python programming, modular development and data processing
Backend Developer	Application logic, API integration and JSON processing
Java Developer	Incident analysis concepts, service failures and backend troubleshooting
Data Engineer	Log processing, data extraction and transformation
Technical Support Engineer	Error investigation, evidence analysis and troubleshooting
Technology Operations	Incident classification, escalation and reporting
DevOps Engineer	Application monitoring concepts and incident investigation
AI Application Developer	Gemini API integration and AI-assisted analysis

The project also provides practical exposure to programming, software architecture, API integration, problem-solving, and automated testing.

---

## 👨‍💻 19. Author

Kartik Mathpati

B.Tech – Computer Engineering

Pune, India

Connect

* GitHub Profile: Kartik2473
* Project Repository: PayGuard AI

---

## 📌 Final Note

PayGuard AI demonstrates how Python-based log processing, rule-based incident classification, event correlation, and Generative AI can be combined to support software troubleshooting and technology operations.

The project focuses on building a practical incident investigation tool that helps engineers understand application failures, review supporting evidence, identify potential causes, and prioritize troubleshooting activities.

It is a prototype intended for learning, demonstration, and further development. It is not a production payment monitoring or automated remediation platform.

Built with Python, Streamlit, and Google Gemini API.
