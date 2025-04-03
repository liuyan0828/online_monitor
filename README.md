# 📊 Online Monitor - Real-time Web Monitoring with Playwright & Python

A complete **web page monitoring automation project** based on **Playwright (Python)**, designed to verify key functionalities and element visibility of [Sohu Sports](https://sports.sohu.com) homepage in real-time.

The project follows **POM (Page Object Model)** structure and integrates **Pytest** with **custom HTML reports, logs, screenshots, and retry mechanism** — ready to be used in production monitoring or automated test pipelines.

---

## 🚀 Features

- **Homepage Navigation Validation**
  - Verify navigation bar item visibility and text correctness
- **Search Functionality Monitoring**
  - Validate placeholder text exists dynamically
  - Click search icon to trigger search and verify URL & content
  - Input keywords & validate search result redirection
- **Advertisement Monitoring**
  - Ensure ad banners are visible, clickable, and redirect correctly
  - Validate image source and HTTP status code
- **Tab Content Verification**
  - Confirm NBA ranking tabs switch correctly and content changes
  - Perform screenshot comparison for visual difference
- **Page Scroll Check**
  - Scroll to bottom and verify dynamic content loads correctly
- **Link Health Check**
  - Extract all page URLs and validate HTTP status (with retry & logs)
- **Reporting**
  - HTML test report auto-generated
  - Screenshot capture on failure
  - Detailed logs for failure analysis

---

## 🛠️ Tech Stack

| Technology      | Purpose                                    |
|-----------------|--------------------------------------------|
| Python         | Programming Language                        |
| Playwright     | Web Automation Framework (async API)        |
| Pytest         | Test Execution & Assertions                 |
| Pytest-HTML    | Custom HTML Reporting                       |
| Asyncio        | Asynchronous execution                      |
| POM Structure  | Project scalability and maintainability     |

---

## 📄 Project Structure

```plaintext
online_monitor/
├── pages/                         # Page Object layer (POM)
│   └── sports_page.py             # Sohu Sports page actions
├── tests/                         # Test cases
│   ├── test_mainpage.py           # Homepage navigation & content test
│   ├── test_search.py             # Search box monitoring test
│   ├── test_ad_banner.py          # Ad banner visibility & redirection test
│   ├── test_tab.py                # NBA tab switching visual check
│   └── test_check_links.py        # URL health check
├── utils/                         # Utility functions
│   └── image_compare.py           # Screenshot comparison helper
├── reports/                       # Generated HTML test reports
├── logs/                          # Log files
├── screenshots/                   # Screenshots captured on failure
├── conftest.py                    # Pytest shared fixtures (browser, context, page)
├── pytest.ini                     # Pytest configuration file
├── main.py                        # One-click test execution entry
└── README.md                      # Project documentation
```

## 📥 Installation

1. Clone the repository:

```bash
git clone https://github.com/liuyan0828/online_monitor.git
cd online_monitor
```

2. Install dependencies:

```bash
pip install -r requirements.txt
playwright install
```

## 🚦 How to Run

Run all test cases:

```bash
pytest tests/ -s
```

Run with HTML report:

```bash
pytest tests/ --alluredir=./allure-results
allure serve ./allure-results
```

## ✅ Usage Scenarios

- Continuous monitoring of key pages' availability
- Daily automated validation
- Functional verification for content and advertisement sections
- Pre-release regression testing

---
