import type { Selector } from '../utils/selector-types';

export type LoginSelectorMap = {
  username: Selector | Selector[];
  password: Selector | Selector[];
  submit: Selector | Selector[];
  error: Selector | Selector[];
};

export const LoginSelectors: LoginSelectorMap = {
  // prefer accessible selectors first (label/role). provide fallback CSS if needed.
  username: [{ kind: 'label', label: 'Username' }, { kind: 'css', value: 'input[name="username"]' }],
  password: [{ kind: 'label', label: 'Password' }, { kind: 'css', value: 'input[name="password"]' }],
  submit: [{ kind: 'role', role: 'button', name: 'Sign in' }, { kind: 'css', value: 'button[type="submit"]' }],
  error: [{ kind: 'css', value: '.alert-error' }, { kind: 'text', text: 'Invalid credentials' }]
};

// dynamic factory example
export const userRowFactory = (username: string): Selector => ({ kind: 'xpath', value: `//tr[.//td[text()="${username}"]]` });
