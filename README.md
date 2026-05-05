# PRODIGY_ST_02 — Compatibility Testing for a Basic Web Page

**Prodigy InfoTech | Software Testing Internship | Task 02**  
**Author:** [Shihab157](https://github.com/Shihab157)

---

## 📌 Task Description

Test a simple web page across different browsers (Chrome, Firefox, Safari, Edge) and devices (desktop, tablet, mobile). Check for layout issues, broken links, and functionality discrepancies. Document findings and recommend fixes in Markdown.

**Target:** [Shoplane E-Commerce Demo](https://shoplane-by-lassie.netlify.app/)

---

## 🗂️ Project Structure

```
PRODIGY_ST_02/
├── tests/
│   └── compatibility_test.py         # 10 test cases × 6 browser/device configs
├── reports/
│   ├── generate_report.py            # Generates HTML report from results.json
│   ├── results.json                  # Auto-generated test results
│   └── test_report.html              # HTML visual report (open in browser)
├── docs/
│   └── compatibility_findings.md     # ⭐ Main deliverable: bugs + fix recommendations
├── requirements.txt
└── README.md
```

---

## ✅ Test Cases

| ID | Test Case | What It Checks |
|----|-----------|----------------|
| TC-01 | Page Load & Title | Site loads, title is non-empty |
| TC-02 | Navbar Visible | Navigation bar renders correctly |
| TC-03 | Hero/Banner Renders | Main banner section is displayed |
| TC-04 | Product Cards Visible | Product listings appear |
| TC-05 | Images Load (No Broken) | All images have `naturalWidth > 0` |
| TC-06 | No Horizontal Scroll | `scrollWidth ≤ windowWidth` |
| TC-07 | Footer Visible | Footer renders after scroll |
| TC-08 | Broken Links Check | Internal links return non-404 |
| TC-09 | No Overflow Elements | No element bleeds beyond viewport |
| TC-10 | Font Rendering | Text ≥ 8px (not invisible) |

---

## 🌐 Browser & Device Matrix

| Config | Device Type | Viewport |
|--------|-------------|----------|
| Chrome – Windows 11 | Desktop | 1366×768 |
| Firefox – Windows 11 | Desktop | 1366×768 |
| Safari – macOS Sonoma | Desktop | 1366×768 |
| Edge – Windows 11 | Desktop | 1366×768 |
| Chrome | Tablet | 768×1024 |
| Chrome | Mobile | 375×812 |

---

## 📊 Results

| Metric | Value |
|--------|-------|
| Total Tests | 60 |
| ✅ Passed | 52 |
| ⚠️ Warnings | 2 |
| ❌ Failed | 6 |
| Pass Rate | 87% |

---

## 🐛 Bugs Found

| ID | Severity | Browser | Device | Issue |
|----|----------|---------|--------|-------|
| BUG-01 | 🔴 High | Safari | Desktop | Horizontal overflow (36px) |
| BUG-02 | 🔴 High | Safari | Desktop | 2 product images broken |
| BUG-03 | 🟡 Medium | Safari | Desktop | Product container overflow |
| BUG-04 | 🔴 High | Chrome | Mobile | No hamburger menu |
| BUG-05 | 🔴 High | Chrome | Mobile | Mobile layout overflow (45px) |
| WARN-01 | 🔵 Low | Chrome | Tablet | Nav links slightly clipped |

See **[`docs/compatibility_findings.md`](docs/compatibility_findings.md)** for full details and CSS/HTML fix recommendations.

---

## 🚀 Setup & Run

```bash
# Install
pip install -r requirements.txt

# Set credentials
set BS_USERNAME=your_username
set BS_ACCESS_KEY=your_access_key

# Run tests
python tests/compatibility_test.py

# Generate HTML report
python reports/generate_report.py
```

---

## 🛠️ Tools

- Python 3.x · Selenium 4 · BrowserStack Automate

---

*Prodigy InfoTech Software Testing Internship — Task 02*
