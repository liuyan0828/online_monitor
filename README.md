# Online Monitor

## 📄 Project Overview

**Online Monitor** is an automated monitoring and validation project based on Playwright and Pytest. It is designed to verify the correctness, availability, and stability of specific webpage content and interactive features. This tool helps ensure the normal display and availability of key functional modules such as navigation, login, search, advertisement, and content cards.

## 🚀 Features

- **Homepage Validation**
  - Verify the presence and visibility of navigation bar elements.
  - Verify login button visibility.
  - Validate the placeholder content and search box functionality.
  - Click on search icon and verify redirection URL.

- **Dynamic Content Testing**
  - Scroll to the bottom of the page and verify footer content.
  - Swipe and verify content cards.
  - Switch tabs and confirm active state and tab content.

- **Advertisement Verification**
  - Detect if advertisement containers are displayed.
  - Verify if ads have valid clickable links.
  - Request ad URL and verify the HTTP status code is 200.

- **Broken Link Checker**
  - Crawl all URLs on the page and validate the returned HTTP status codes.

- **Visual Validation (Optional)**
  - Screenshot key modules and compare for regression testing.

## 🛠️ Tech Stack

- **Playwright**: Web automation and testing framework.
- **Pytest**: Python testing framework.
- **pytest-asyncio**: Supports writing asynchronous test cases.
- **Ruff**: Python linter for code style and quality.
- **Allure** (optional): For generating HTML reports.

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

## 📄 Directory Structure

```
online_monitor/
├── tests/                      # Test cases
│   └── test_mainpage.py        # Main Page Validation
├── main.py                     # Entry point for manual run
├── conftest.py                 # Pytest configuration
├── pytest.ini                  # Pytest settings
├── playwright.config.json      # Playwright settings
├── requirements.txt            # Dependencies
└── README.md                   # Project Description
```

## ✅ Usage Scenarios

- Continuous monitoring of key pages' availability
- Daily automated validation
- Functional verification for content and advertisement sections
- Pre-release regression testing

---