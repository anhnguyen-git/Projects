# Playwright POM TS (Advanced)

Scaffold with per-page selectors and a flexible locator resolver that supports:
- role (getByRole), label (getByLabel), placeholder, text, data-testid, css, xpath and custom resolvers
- fallback arrays: try multiple selector strategies in order
- Selector factory functions for dynamic selectors

Install and run:
```bash
npm install
npx playwright install --with-deps
npm test
```
