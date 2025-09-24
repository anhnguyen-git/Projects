import type { SelectorFactory } from './selector-types';

export const xpathContaining: SelectorFactory = (params) => {
  const value = params?.value ?? '';
  const escaped = String(value).replace(/"/g, '\\"');
  return { kind: 'xpath', value: `//div[contains(normalize-space(.),"${escaped}")]` };
};

export const rowByText: SelectorFactory = (params) => ({ kind: 'text', text: String(params?.text ?? '') });
