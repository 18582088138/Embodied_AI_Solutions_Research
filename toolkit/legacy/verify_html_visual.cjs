// Optional visual QA: uses the bundled Playwright runtime; blocks all remote requests.
const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { chromium } = require('playwright');
(async () => {
  const [input, output] = process.argv.slice(2);
  if (!input || !output) throw new Error('Usage: node verify_html_visual.cjs input.html preview.png');
  const candidates = process.platform === 'win32' ? [
    path.join(process.env['ProgramFiles(x86)'] || '', 'Microsoft/Edge/Application/msedge.exe'),
    path.join(process.env.ProgramFiles || '', 'Google/Chrome/Application/chrome.exe'),
  ] : [];
  const executablePath = candidates.find(candidate => fs.existsSync(candidate));
  const browser = await chromium.launch({ headless: true, ...(executablePath ? { executablePath } : {}) });
  try {
    const page = await browser.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
    const styleResponses = new Map();
    page.on('response', response => {
      if (response.request().resourceType() === 'stylesheet') styleResponses.set(response.url(), { status: response.status(), ok: response.ok() });
    });
    await page.route(/^https?:\/\//, route => route.abort());
    await page.goto(pathToFileURL(path.resolve(input)).href, { waitUntil: 'load', timeout: 30000 });
    await page.screenshot({ path: path.resolve(output), fullPage: false });
    const summary = await page.evaluate(() => ({
      title: document.title, headings: [...document.querySelectorAll('h1,h2')].map(n => n.textContent.trim()).slice(0, 12),
      readableTextChars: document.body.innerText.length,
      localStylesheets: [...document.querySelectorAll('link[rel=stylesheet]')].map(n => {
        let rules = null;
        try { rules = n.sheet ? n.sheet.cssRules.length : 0; } catch (_) {}
        return { href: n.href, local: n.href.startsWith('file:'), ruleCount: rules, sheetPresent: !!n.sheet, cssomRestricted: rules === null };
      }),
      documentHeight: document.documentElement.scrollHeight,
    }));
    summary.localStylesheets = summary.localStylesheets.map(sheet => ({ ...sheet,
      response: styleResponses.get(sheet.href) || null,
      loaded: styleResponses.has(sheet.href) ? styleResponses.get(sheet.href).ok && sheet.sheetPresent : null,
    }));
    fs.writeFileSync(output + '.json', JSON.stringify(summary, null, 2));
    console.log(JSON.stringify(summary));
  } finally { await browser.close(); }
})().catch(error => { console.error(error.message); process.exit(1); });
