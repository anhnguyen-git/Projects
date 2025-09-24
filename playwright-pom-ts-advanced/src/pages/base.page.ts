import type { Page, Locator } from '@playwright/test';
import { resolveLocator, resolveWithFallback } from '../utils/locator-helper';
import type { Selector, SelectorFactory } from '../utils/selector-types';

export default class BasePage {
  readonly page: Page;

  constructor(page: Page) {
    this.page = page;
  }

  // Accept a Selector, an array of Selectors (fallback), or a factory function
  protected async getLocator(sel: Selector | Selector[] | SelectorFactory | ((...args: any[]) => Selector), params?: Record<string, string | number>): Promise<Locator> {
    let selectorOrArray: Selector | Selector[];
    if (typeof sel === 'function') {
      selectorOrArray = (sel as SelectorFactory)(params);
    } else {
      selectorOrArray = sel as Selector | Selector[];
    }

    if (Array.isArray(selectorOrArray)) {
      return await resolveWithFallback(this.page, selectorOrArray);
    } else {
      return resolveLocator(this.page, selectorOrArray);
    }
  }

  async click(sel: Selector | Selector[] | SelectorFactory, params?: Record<string, string | number>) {
    const locator = await this.getLocator(sel as any, params);
    await locator.click();
  }

  async fill(sel: Selector | Selector[] | SelectorFactory, value: string, params?: Record<string, string | number>) {
    const locator = await this.getLocator(sel as any, params);
    await locator.fill(value);
  }

  async getText(sel: Selector | Selector[] | SelectorFactory, params?: Record<string, string | number>): Promise<string | null> {
    const locator = await this.getLocator(sel as any, params);
    const t = await locator.textContent();
    return t?.trim() ?? null;
  }

  async isVisible(sel: Selector | Selector[] | SelectorFactory, params?: Record<string, string | number>): Promise<boolean> {
    const locator = await this.getLocator(sel as any, params);
    return await locator.isVisible();
  }

  // expose locator for advanced ops
  async locator(sel: Selector | Selector[] | SelectorFactory, params?: Record<string, string | number>): Promise<Locator> {
    return await this.getLocator(sel as any, params);
  }

  async goto(path: string) {
    await this.page.goto(path);
  }
}
