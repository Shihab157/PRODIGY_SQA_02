"""
Task-02: Compatibility Testing for a Basic Web Page
Author  : Shihab157
Repo    : PRODIGY_ST_02
Target  : https://shoplane-by-lassie.netlify.app/

Checks layout issues, broken links, and functionality discrepancies
across browsers (Chrome, Firefox, Safari, Edge) and
devices (Desktop, Tablet, Mobile) via BrowserStack.
"""

import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, WebDriverException
)

# ── BrowserStack credentials ──────────────────────────────────────────────────
BS_USERNAME   = os.environ.get("BS_USERNAME",   "YOUR_BROWSERSTACK_USERNAME")
BS_ACCESS_KEY = os.environ.get("BS_ACCESS_KEY", "YOUR_BROWSERSTACK_ACCESS_KEY")
BS_HUB = f"https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

URL = "https://shoplane-by-lassie.netlify.app/"

# ── Browser + Device Matrix ───────────────────────────────────────────────────
# Covers: Desktop (3 browsers), Tablet (1), Mobile (1)
CONFIGS = [
    # ── Desktop ───────────────────────────────────────────────────────────────
    {
        "browser": "chrome", "browser_version": "latest",
        "os": "Windows", "os_version": "11",
        "name": "Chrome – Desktop (Win11)",
        "viewport": (1366, 768), "device_type": "Desktop"
    },
    {
        "browser": "firefox", "browser_version": "latest",
        "os": "Windows", "os_version": "11",
        "name": "Firefox – Desktop (Win11)",
        "viewport": (1366, 768), "device_type": "Desktop"
    },
    {
        "browser": "safari", "browser_version": "17",
        "os": "OS X", "os_version": "Sonoma",
        "name": "Safari – Desktop (macOS Sonoma)",
        "viewport": (1366, 768), "device_type": "Desktop"
    },
    {
        "browser": "edge", "browser_version": "latest",
        "os": "Windows", "os_version": "11",
        "name": "Edge – Desktop (Win11)",
        "viewport": (1366, 768), "device_type": "Desktop"
    },
    # ── Tablet ────────────────────────────────────────────────────────────────
    {
        "browser": "chrome", "browser_version": "latest",
        "os": "Windows", "os_version": "11",
        "name": "Chrome – Tablet (768×1024)",
        "viewport": (768, 1024), "device_type": "Tablet"
    },
    # ── Mobile ────────────────────────────────────────────────────────────────
    {
        "browser": "chrome", "browser_version": "latest",
        "os": "Windows", "os_version": "11",
        "name": "Chrome – Mobile (375×812)",
        "viewport": (375, 812), "device_type": "Mobile"
    },
]

# ── All internal links to check ───────────────────────────────────────────────
INTERNAL_LINKS = [
    "/",
    "/#men",
    "/#women",
    "/#kids",
]


# ── Driver factory ────────────────────────────────────────────────────────────
def get_driver(cfg: dict) -> webdriver.Remote:
    caps = {
        "bstack:options": {
            "userName":    BS_USERNAME,
            "accessKey":   BS_ACCESS_KEY,
            "projectName": "PRODIGY_ST_02",
            "buildName":   "Shoplane Compatibility Suite",
            "sessionName": cfg["name"],
            "debug":       True,
            "consoleLogs": "info",
            "networkLogs": True,
        },
        "browserName":    cfg["browser"],
        "browserVersion": cfg["browser_version"],
        "os":             cfg["os"],
        "osVersion":      cfg["os_version"],
    }
    driver = webdriver.Remote(command_executor=BS_HUB, desired_capabilities=caps)
    w, h = cfg["viewport"]
    driver.set_window_size(w, h)
    driver.implicitly_wait(10)
    return driver


def mark_session(driver, status: str, reason: str):
    driver.execute_script(
        f'browserstack_executor: {{"action":"setSessionStatus",'
        f'"arguments":{{"status":"{status}","reason":"{reason}"}}}}'
    )


# ── Test Suite ────────────────────────────────────────────────────────────────
class ShoplaneCompatibilityTests:

    def __init__(self, driver, cfg: dict):
        self.driver      = driver
        self.cfg         = cfg
        self.name        = cfg["name"]
        self.device_type = cfg["device_type"]
        self.wait        = WebDriverWait(driver, 15)
        self.results     = []

    def _log(self, tc: str, status: str, notes: str = ""):
        icon = "✅" if status == "PASS" else ("⚠️" if status == "WARN" else "❌")
        print(f"  {icon} [{self.name}] {tc}: {status}  {notes}")
        self.results.append({
            "config":      self.name,
            "device_type": self.device_type,
            "test":        tc,
            "status":      status,
            "notes":       notes,
        })

    # TC-01 ── Page load & title ───────────────────────────────────────────────
    def tc01_page_load(self):
        try:
            self.driver.get(URL)
            title = self.driver.title
            assert title and len(title) > 0
            self._log("TC-01 Page Load & Title", "PASS", f"title='{title[:60]}'")
        except Exception as e:
            self._log("TC-01 Page Load & Title", "FAIL", str(e))

    # TC-02 ── Navbar visible & links present ─────────────────────────────────
    def tc02_navbar(self):
        try:
            self.driver.get(URL)
            # Try common navbar selectors
            navbar = None
            for sel in ["nav", ".navbar", ".nav", "header", "#navbar"]:
                try:
                    navbar = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if navbar.is_displayed():
                        break
                except NoSuchElementException:
                    continue
            if navbar and navbar.is_displayed():
                self._log("TC-02 Navbar Visible", "PASS")
            else:
                self._log("TC-02 Navbar Visible", "WARN", "Navbar element not found via common selectors")
        except Exception as e:
            self._log("TC-02 Navbar Visible", "FAIL", str(e))

    # TC-03 ── Hero / Banner section renders ──────────────────────────────────
    def tc03_hero_section(self):
        try:
            self.driver.get(URL)
            # Look for hero/banner image or section
            hero = None
            for sel in [".hero", ".banner", ".carousel", ".slider",
                        "section img", ".hero-section", "#hero"]:
                try:
                    hero = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if hero.is_displayed():
                        break
                except NoSuchElementException:
                    continue
            if hero and hero.is_displayed():
                self._log("TC-03 Hero/Banner Renders", "PASS")
            else:
                self._log("TC-03 Hero/Banner Renders", "WARN",
                          "No hero section found — may use different class name")
        except Exception as e:
            self._log("TC-03 Hero/Banner Renders", "FAIL", str(e))

    # TC-04 ── Product cards visible ──────────────────────────────────────────
    def tc04_product_cards(self):
        try:
            self.driver.get(URL)
            time.sleep(2)  # allow JS to render products
            # Try multiple product card selectors
            cards = []
            for sel in [".card", ".product", ".product-card",
                        ".item", "[class*='card']", "[class*='product']"]:
                cards = self.driver.find_elements(By.CSS_SELECTOR, sel)
                if len(cards) > 0:
                    break
            if len(cards) >= 1:
                self._log("TC-04 Product Cards Visible", "PASS",
                          f"{len(cards)} card(s) found")
            else:
                self._log("TC-04 Product Cards Visible", "WARN",
                          "No product cards detected (JS may still be loading)")
        except Exception as e:
            self._log("TC-04 Product Cards Visible", "FAIL", str(e))

    # TC-05 ── Images load (no broken images) ─────────────────────────────────
    def tc05_images(self):
        try:
            self.driver.get(URL)
            time.sleep(2)
            imgs = self.driver.find_elements(By.TAG_NAME, "img")
            broken = []
            for img in imgs:
                natural_width = self.driver.execute_script(
                    "return arguments[0].naturalWidth;", img
                )
                src = img.get_attribute("src") or ""
                if natural_width == 0 and src:
                    broken.append(src[-60:])  # last 60 chars of src

            if not broken:
                self._log("TC-05 Images Load (No Broken)", "PASS",
                          f"{len(imgs)} image(s) checked")
            else:
                self._log("TC-05 Images Load (No Broken)", "FAIL",
                          f"{len(broken)} broken: {broken[0]}")
        except Exception as e:
            self._log("TC-05 Images Load (No Broken)", "FAIL", str(e))

    # TC-06 ── Horizontal scrollbar should NOT appear on desktop ──────────────
    def tc06_no_horizontal_scroll(self):
        try:
            self.driver.get(URL)
            time.sleep(1)
            scroll_width  = self.driver.execute_script("return document.body.scrollWidth;")
            window_width  = self.driver.execute_script("return window.innerWidth;")
            if scroll_width > window_width + 5:   # 5px tolerance
                self._log("TC-06 No Horizontal Scroll", "FAIL",
                          f"scrollWidth={scroll_width} > windowWidth={window_width} → layout overflow")
            else:
                self._log("TC-06 No Horizontal Scroll", "PASS",
                          f"scrollWidth={scroll_width}, windowWidth={window_width}")
        except Exception as e:
            self._log("TC-06 No Horizontal Scroll", "FAIL", str(e))

    # TC-07 ── Footer visible ─────────────────────────────────────────────────
    def tc07_footer(self):
        try:
            self.driver.get(URL)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            footer = None
            for sel in ["footer", ".footer", "#footer"]:
                try:
                    footer = self.driver.find_element(By.CSS_SELECTOR, sel)
                    if footer.is_displayed():
                        break
                except NoSuchElementException:
                    continue
            if footer and footer.is_displayed():
                self._log("TC-07 Footer Visible", "PASS")
            else:
                self._log("TC-07 Footer Visible", "WARN", "Footer element not found")
        except Exception as e:
            self._log("TC-07 Footer Visible", "FAIL", str(e))

    # TC-08 ── Links: check for 404 via JS fetch ──────────────────────────────
    def tc08_link_check(self):
        try:
            self.driver.get(URL)
            time.sleep(1)
            anchors = self.driver.find_elements(By.TAG_NAME, "a")
            hrefs = []
            for a in anchors:
                href = a.get_attribute("href") or ""
                if href.startswith("http") and "shoplane" in href and href not in hrefs:
                    hrefs.append(href)

            broken_links = []
            for href in hrefs[:10]:  # check up to 10 internal links
                status = self.driver.execute_script("""
                    var xhr = new XMLHttpRequest();
                    xhr.open('HEAD', arguments[0], false);
                    try { xhr.send(); return xhr.status; }
                    catch(e) { return 0; }
                """, href)
                if status in (404, 0):
                    broken_links.append(f"{href[-50:]} ({status})")

            if broken_links:
                self._log("TC-08 Broken Links Check", "FAIL",
                          f"Broken: {', '.join(broken_links)}")
            else:
                self._log("TC-08 Broken Links Check", "PASS",
                          f"{len(hrefs)} internal link(s) checked — all OK")
        except Exception as e:
            self._log("TC-08 Broken Links Check", "FAIL", str(e))

    # TC-09 ── Responsive: key elements still visible at viewport ─────────────
    def tc09_responsive_elements(self):
        try:
            self.driver.get(URL)
            time.sleep(1.5)
            body = self.driver.find_element(By.TAG_NAME, "body")
            assert body.is_displayed()
            # Check no element bleeds beyond viewport
            overflow = self.driver.execute_script("""
                var elems = document.querySelectorAll('*');
                var vw = window.innerWidth;
                var bad = [];
                for(var i=0; i<Math.min(elems.length,200); i++){
                    var r = elems[i].getBoundingClientRect();
                    if(r.right > vw + 5){ bad.push(elems[i].tagName+'.'+elems[i].className.split(' ')[0]); }
                }
                return bad.slice(0,5);
            """)
            if overflow:
                self._log("TC-09 Responsive – No Overflow Elements", "FAIL",
                          f"Overflow: {', '.join(overflow)}")
            else:
                self._log("TC-09 Responsive – No Overflow Elements", "PASS")
        except Exception as e:
            self._log("TC-09 Responsive – No Overflow Elements", "FAIL", str(e))

    # TC-10 ── Font rendering (not invisible/tiny) ────────────────────────────
    def tc10_font_rendering(self):
        try:
            self.driver.get(URL)
            # Find first visible paragraph or heading
            for sel in ["h1", "h2", "h3", "p", ".title", ".heading"]:
                try:
                    el = self.driver.find_element(By.CSS_SELECTOR, sel)
                    size = self.driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).fontSize;", el
                    )
                    size_px = float(size.replace("px", "")) if size else 0
                    if size_px < 8:
                        self._log("TC-10 Font Rendering", "FAIL",
                                  f"Font too small: {size_px}px on <{sel}>")
                    else:
                        self._log("TC-10 Font Rendering", "PASS",
                                  f"{sel} fontSize={size}")
                    return
                except NoSuchElementException:
                    continue
            self._log("TC-10 Font Rendering", "WARN", "No heading/paragraph found to measure")
        except Exception as e:
            self._log("TC-10 Font Rendering", "FAIL", str(e))

    def run_all(self):
        print(f"\n{'='*65}")
        print(f"  {self.name}  [{self.device_type}  {self.cfg['viewport']}]")
        print(f"{'='*65}")
        self.tc01_page_load()
        self.tc02_navbar()
        self.tc03_hero_section()
        self.tc04_product_cards()
        self.tc05_images()
        self.tc06_no_horizontal_scroll()
        self.tc07_footer()
        self.tc08_link_check()
        self.tc09_responsive_elements()
        self.tc10_font_rendering()
        return self.results


# ── Main runner ───────────────────────────────────────────────────────────────
def run():
    all_results = []
    for cfg in CONFIGS:
        driver = None
        try:
            print(f"\n🚀  Starting: {cfg['name']}")
            driver  = get_driver(cfg)
            suite   = ShoplaneCompatibilityTests(driver, cfg)
            results = suite.run_all()
            all_results.extend(results)
            fails = [r for r in results if r["status"] == "FAIL"]
            mark_session(driver,
                         "failed" if fails else "passed",
                         f"{len(fails)} failure(s)" if fails else "All tests passed")
        except Exception as e:
            print(f"  ❌ Session error ({cfg['name']}): {e}")
            all_results.append({
                "config": cfg["name"], "device_type": cfg["device_type"],
                "test": "Session Setup", "status": "ERROR", "notes": str(e)
            })
        finally:
            if driver:
                driver.quit()

    os.makedirs("reports", exist_ok=True)
    with open("reports/results.json", "w") as f:
        json.dump(all_results, f, indent=2)

    passed = sum(1 for r in all_results if r["status"] == "PASS")
    warns  = sum(1 for r in all_results if r["status"] == "WARN")
    failed = sum(1 for r in all_results if r["status"] in ("FAIL", "ERROR"))
    print(f"\n{'='*65}")
    print(f"  DONE  |  ✅ {passed} passed  |  ⚠️ {warns} warnings  |  ❌ {failed} failed")
    print(f"  Results → reports/results.json")
    print(f"{'='*65}")


if __name__ == "__main__":
    run()
