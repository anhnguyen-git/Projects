import type { Page, Locator } from '@playwright/test';
import type { Selector } from './selector-types';

// Convert a single Selector into a Playwright Locator (no fallback logic here)
export function resolveLocator(page: Page, selector: Selector): Locator {
  switch (selector.kind) {
    case 'css':
      return page.locator(selector.value);
    case 'xpath':
      return page.locator(`xpath=${selector.value}`);
    case 'role': {
      const opts: any = {};
      if (selector.name !== undefined) opts.name = selector.name;
      if ((selector as any).checked !== undefined) opts.checked = (selector as any).checked;
      if ((selector as any).selected !== undefined) opts.selected = (selector as any).selected;
      if ((selector as any).pressed !== undefined) opts.pressed = (selector as any).pressed;
      if ((selector as any).expanded !== undefined) opts.expanded = (selector as any).expanded;
      if ((selector as any).level !== undefined) opts.level = (selector as any).level;
      return page.getByRole(selector.role, Object.keys(opts).length ? opts : undefined);
    }
    case 'label':
      return page.getByLabel(selector.label);
    case 'placeholder':
      return page.getByPlaceholder(selector.placeholder);
    case 'text':
      return page.getByText(selector.text);
    case 'testid':
      // Use data-testid attribute matcher (common pattern)
      return page.locator(`[data-testid="${selector.id}"]`);
    case 'custom':
      return selector.resolver(page);
    default: {
      const _exhaustive: never = selector as never;
      throw new Error('Unsupported selector kind: ' + JSON.stringify(_exhaustive));
    }
  }
}

// Try multiple selectors (fallback sequence). Returns the first Locator that matches an element.
export async function resolveWithFallback(page: Page, selectors: Selector[]): Promise<Locator> {
  for (const s of selectors) {
    const loc = resolveLocator(page, s);
    try {
      const count = await loc.count();
      if (count > 0) return loc.first();
    } catch (e) {
      // ignore and continue to next strategy
    }
  }
  // If none matched, return the locator for the first strategy (so calling code can act and fail with a useful error)
  return resolveLocator(page, selectors[0]);
}
