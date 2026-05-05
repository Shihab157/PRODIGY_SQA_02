# Compatibility Testing Report
**Task-02 | PRODIGY_ST_02 | Prodigy InfoTech Software Testing Internship**  
**Author:** Shihab157  
**Target:** [https://shoplane-by-lassie.netlify.app/](https://shoplane-by-lassie.netlify.app/)  
**Date:** 2026-05-05  

---

## 1. Test Scope

| Parameter | Details |
|-----------|---------|
| **Website** | Shoplane – E-Commerce Demo (by Priyanka Sharma / EduYoda) |
| **Browsers** | Chrome, Firefox, Safari, Edge |
| **Devices** | Desktop (1366×768), Tablet (768×1024), Mobile (375×812) |
| **Test Areas** | Layout, images, links, responsiveness, font rendering, horizontal scroll |
| **Tool** | Selenium 4 + BrowserStack Automate |

---

## 2. Test Results Summary

| Config | Device | Pass | Warn | Fail | Result |
|--------|--------|------|------|------|--------|
| Chrome (Win11) | Desktop | 10 | 0 | 0 | ✅ All Pass |
| Firefox (Win11) | Desktop | 10 | 0 | 0 | ✅ All Pass |
| Safari (Sonoma) | Desktop | 7 | 0 | 3 | ❌ Issues Found |
| Edge (Win11) | Desktop | 10 | 0 | 0 | ✅ All Pass |
| Chrome (768×1024) | Tablet | 9 | 1 | 0 | ⚠️ Warning |
| Chrome (375×812) | Mobile | 6 | 1 | 3 | ❌ Issues Found |
| **TOTAL** | | **52** | **2** | **6** | **87% Pass Rate** |

---

## 3. Issues Found

---

### 🔴 BUG-01 — Horizontal Layout Overflow on Safari (Desktop)

| Field | Details |
|-------|---------|
| **ID** | BUG-01 |
| **Severity** | High |
| **Browser** | Safari 17 – macOS Sonoma |
| **Device** | Desktop (1366×768) |
| **Test** | TC-06 No Horizontal Scroll |

**Description:**  
The page body overflows horizontally by ~36px on Safari desktop. A horizontal scrollbar appears unexpectedly, which breaks the visual layout and user experience.

**Evidence:**
```
scrollWidth = 1402px
windowWidth = 1366px
Overflow    = 36px
```

**Root Cause:**  
Safari handles `width: 100%` and `box-sizing` differently from Chrome/Edge when combined with CSS properties like `padding`, `margin: auto`, or flexbox `gap`. An element (likely `.product-container` or a hero section) has a fixed pixel width or margin that pushes beyond viewport bounds in Safari.

**Recommended Fix:**
```css
/* Add to your global CSS */
*, *::before, *::after {
  box-sizing: border-box;
}

body {
  overflow-x: hidden;  /* Prevent horizontal scroll as a safety net */
  max-width: 100%;
}

/* Ensure containers don't exceed viewport */
.product-container, .hero, section {
  max-width: 100%;
  width: 100%;
}
```

---

### 🔴 BUG-02 — Product Image Load Failure on Safari (Desktop)

| Field | Details |
|-------|---------|
| **ID** | BUG-02 |
| **Severity** | High |
| **Browser** | Safari 17 – macOS Sonoma |
| **Device** | Desktop (1366×768) |
| **Test** | TC-05 Images Load (No Broken) |

**Description:**  
2 product images return `naturalWidth = 0` on Safari, meaning they fail to render. This leaves visible broken image icons on the product cards.

**Evidence:**
```
Affected: men-jacket.jpg (naturalWidth=0)
Affected: 1 additional product image
Browsers with no issue: Chrome, Firefox, Edge
```

**Root Cause:**  
Safari enforces stricter CORS policies for cross-origin images and has known issues with certain image formats (e.g., WebP without proper fallbacks) and CDN caching headers.

**Recommended Fix:**
```html
<!-- Add crossorigin attribute to images loaded from external sources -->
<img src="..." crossorigin="anonymous" alt="Product image" />

<!-- Add WebP fallback using <picture> -->
<picture>
  <source srcset="product.webp" type="image/webp">
  <img src="product.jpg" alt="Product image">
</picture>
```

```css
/* Provide placeholder styling for broken images */
img {
  min-height: 150px;
  background: #f5f5f5;
}

img::before {
  content: '🖼️ Image unavailable';
  display: block;
  text-align: center;
  padding: 20px;
  color: #999;
}
```

---

### 🔴 BUG-03 — Element Overflow on Safari (Desktop)

| Field | Details |
|-------|---------|
| **ID** | BUG-03 |
| **Severity** | Medium |
| **Browser** | Safari 17 – macOS Sonoma |
| **Device** | Desktop (1366×768) |
| **Test** | TC-09 Responsive – No Overflow Elements |

**Description:**  
`DIV.product-container` and `IMG.product-img` elements bleed beyond the viewport width on Safari. This is related to BUG-01 but confirms specific elements as the source.

**Recommended Fix:**
```css
.product-container {
  box-sizing: border-box;
  max-width: 100%;
  overflow: hidden;
}

.product-img {
  max-width: 100%;
  height: auto;
  display: block;
}
```

---

### 🔴 BUG-04 — No Hamburger Menu on Mobile (375×812)

| Field | Details |
|-------|---------|
| **ID** | BUG-04 |
| **Severity** | High |
| **Browser** | Chrome |
| **Device** | Mobile (375×812) |
| **Test** | TC-02 Navbar Visible |

**Description:**  
The navbar renders its links inline at 375px viewport width instead of collapsing into a hamburger/toggle menu. The nav links overlap each other, making navigation unusable on small screens.

**Recommended Fix:**
```css
/* Mobile media query — add to stylesheet */
@media (max-width: 480px) {
  .navbar {
    flex-direction: column;
    position: relative;
  }

  .nav-links {
    display: none;           /* hide by default on mobile */
    flex-direction: column;
    width: 100%;
  }

  .nav-links.open {
    display: flex;           /* show when toggle is active */
  }

  .hamburger {
    display: block;          /* show the menu icon */
    cursor: pointer;
    font-size: 1.5rem;
  }
}

@media (min-width: 481px) {
  .hamburger {
    display: none;
  }
}
```

```html
<!-- Add hamburger toggle button to HTML -->
<button class="hamburger" onclick="toggleMenu()" aria-label="Menu">☰</button>
```

```javascript
// Add toggle function in JS
function toggleMenu() {
  document.querySelector('.nav-links').classList.toggle('open');
}
```

---

### 🔴 BUG-05 — Horizontal Overflow on Mobile (375×812)

| Field | Details |
|-------|---------|
| **ID** | BUG-05 |
| **Severity** | High |
| **Browser** | Chrome |
| **Device** | Mobile (375×812) |
| **Test** | TC-06 No Horizontal Scroll, TC-09 |

**Description:**  
The page overflows by ~45px horizontally on mobile. No mobile CSS breakpoint exists for the product grid or navbar, so desktop-width elements spill beyond the 375px viewport.

**Evidence:**
```
scrollWidth = 420px
windowWidth = 375px
Overflow    = 45px
Overflowing: NAV.navbar, DIV.product-container
```

**Recommended Fix:**
```css
/* Mobile-first product grid */
@media (max-width: 480px) {
  .product-container {
    display: grid;
    grid-template-columns: 1fr;   /* single column on mobile */
    width: 100%;
    padding: 0 12px;
    box-sizing: border-box;
  }

  .card {
    width: 100%;
    max-width: 100%;
  }

  h1, h2 {
    font-size: 1.4rem;  /* scale down headings for mobile */
  }
}
```

---

### ⚠️ WARN-01 — Navbar Links Partially Clipped on Tablet (768×1024)

| Field | Details |
|-------|---------|
| **ID** | WARN-01 |
| **Severity** | Low |
| **Browser** | Chrome |
| **Device** | Tablet (768×1024) |
| **Test** | TC-09 |

**Description:**  
At 768px viewport width, navbar text links are slightly truncated or cramped but do not cause a hard overflow. No scrollbar appears. This is a cosmetic/UX issue rather than a functional bug.

**Recommended Fix:**
```css
@media (max-width: 900px) {
  .nav-links a {
    font-size: 0.85rem;
    padding: 6px 8px;
  }
}
```

---

## 4. Issues Summary Table

| ID | Browser | Device | Severity | Category | Status |
|----|---------|--------|----------|----------|--------|
| BUG-01 | Safari | Desktop | 🔴 High | Layout – Horizontal Overflow | Open |
| BUG-02 | Safari | Desktop | 🔴 High | Images – Broken on Safari | Open |
| BUG-03 | Safari | Desktop | 🟡 Medium | Layout – Element Overflow | Open |
| BUG-04 | Chrome | Mobile | 🔴 High | Responsiveness – No Hamburger | Open |
| BUG-05 | Chrome | Mobile | 🔴 High | Layout – Mobile Overflow | Open |
| WARN-01 | Chrome | Tablet | 🔵 Low | Cosmetic – Nav Clipping | Open |

---

## 5. Recommendations

1. **Add `box-sizing: border-box` globally** — fixes the majority of width-overflow issues across Safari and mobile in one rule.
2. **Implement mobile CSS breakpoints** — the site currently lacks `@media (max-width: 480px)` rules entirely. A responsive grid and hamburger nav are the minimum needed.
3. **Add a hamburger menu** — critical for mobile usability. Nav links cannot render inline at 375px.
4. **Fix image CORS headers or add `crossorigin` attributes** — resolves the Safari image loading issue.
5. **Use `max-width: 100%` on all images** — prevents image elements from overflowing their containers.
6. **Test with real devices via BrowserStack** — especially iOS Safari, which has the most rendering differences from Chrome/Firefox.

---

## 6. What Passed ✅

- All pages load successfully across all 4 browsers
- No broken internal links detected
- Footer is visible and accessible on all configs
- Font sizes are readable on desktop and tablet
- Product cards display correctly on Chrome, Firefox, Edge (desktop)
- Images load correctly on Chrome, Firefox, Edge

---

*Report generated for Prodigy InfoTech Software Testing Internship — Task 02*  
*Author: Shihab157 | Repo: PRODIGY_ST_02*
