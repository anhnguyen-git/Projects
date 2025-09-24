import type { Page, Locator, AriaRole } from '@playwright/test';

// A Selector describes one strategy to find an element.
export type Selector =
  | { kind: 'css'; value: string }
  | { kind: 'xpath'; value: string }
  | { kind: 'role'; role: AriaRole; name?: string | RegExp; checked?: boolean; selected?: boolean; pressed?: boolean; expanded?: boolean; level?: number }
  | { kind: 'label'; label: string }
  | { kind: 'placeholder'; placeholder: string }
  | { kind: 'text'; text: string }
  | { kind: 'testid'; id: string }
  | { kind: 'custom'; resolver: (page: Page) => Locator };

// A SelectorFactory returns a Selector dynamically (used for rows, items...)
export type SelectorFactory = (params?: Record<string, string | number>) => Selector;
