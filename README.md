# Universal SQL Optimization & Automated Code Review Engine
[![App Status](https://img.shields.io/badge/Live%20Web%20Application-Click%20Here-brightgreen?style=for-the-badge&logo=streamlit)](https://huggingface.co/spaces/namita8584/sql-code-review)

An end-to-end static code analysis tool and interactive analytics dashboard built to identify performance bottlenecks, anti-patterns, and security risks in SQL queries. This application evaluates raw SQL text strings against 12 enterprise-grade linting rules completely independent of a database schema, generating quantitative quality scores and actionable optimization prescriptions.

## Core Features
* **Schema-Agnostic Static Analysis:** Automatically parses raw SQL syntax inputs to detect index-killing predicates, unbounded sorting operations, and structural design risks.
* **Quantitative Quality Scoring:** Features a dynamic grading module that applies weighted deductions based on vulnerability severity (Critical Hazards, Performance Risks, Optimization Tips).
* **Actionable Engineering Prescriptions:** Maps flagged anti-patterns directly to explicit refactoring instructions and structured code remedies.
* **Historical Audit Logging:** Automatically captures performance metadata (timestamps, quality scores, issue volumes) into a persistent CSV repository.
* **Executive BI Dashboard:** A integrated secondary dashboard interface powered by Plotly to track rolling code quality indexes, flaw distribution volumes, and query metrics over time.

## Architectural Enforcement Rules
1. **Wildcard Overhead:** Flags `SELECT *` selections to protect network I/O.
2. **Non-SARGable Functions:** Catches inline scalar functions (e.g., `YEAR()`, `UPPER()`) inside filtering predicates that break B-Tree index scanning.
3. **Leading Wildcards:** Flags sequential table sweep vulnerabilities caused by `LIKE '%text'` arguments.
4. **Join Complexity:** Identifies complex layouts exceeding 4 table links and suggests Common Table Expressions (CTEs).
5. **Unbounded Sorting:** Warns against memory-spooling threats from sorting datasets without a row-capping limit.
6. **Set Operation Latency:** Catches expensive deduplication sorts caused by improper `UNION` usage.
7. **Deep Nesting:** Highlights highly nested inline subqueries affecting compiler execution tracking.
8. **Missing Filters:** Flags global data requests missing conditional constraints.
9. **Null Evaluation Logic:** Identifies syntax logic traps using standard equals operators on NULL attributes.
10. **SQL Injection Risks:** Detects vulnerable dynamic inline variable concatenations.
11. **Global Mutation Risk:** Blocks mass destructive data operations missing protective conditions.
12. **Schema Drop Hazards:** Monitors explicit structure deletions to ensure isolation behind formal migration processes.

## Technical Stack
* **Core Language:** Python 3.10+
* **Framework & UI Layout:** Streamlit
* **Data Processing & Analytics:** Pandas
* **Data Visualization:** Plotly Express
* **Abstract Syntax Tree Parsing:** SQLParse

## File Architecture
sql-review-assistant/
├── streamlit_app.py      # Main User Interface & Analysis Hub (Hugging Face Entry)
├── dashboard.py          # BI Analytics Monitoring Console
├── sql_analyzer.py       # Core Text Parser & 12 Heuristics
├── scoring.py            # Quantitative Grading Evaluation Logic
├── recommendations.py    # Prescriptive Engineering Remedies
├── ai_explainer.py       # Glossary & NLP Pipeline Layer
├── reviews.csv           # Persistent Metadata Evaluation Log
├── Dockerfile            # Enterprise Cloud Deployment Container
└── requirements.txt      # Platform-Agnostic Dependency Registry

## How To Run The Applications

1. Launch the Core Code Review Assistant Portal locally:
   streamlit run streamlit_app.py --server.headless true

2. Launch the BI Executive Analytics Dashboard Panel locally:
   streamlit run dashboard.py --server.port 8502 --server.headless true

## How To Run The Applications

1. Launch the Core Code Review Assistant Portal:
   streamlit run app.py --server.headless true

2. Launch the BI Executive Analytics Dashboard Panel:
   streamlit run dashboard.py --server.port 8502 --server.headless true
