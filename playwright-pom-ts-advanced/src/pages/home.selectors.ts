import type { Selector } from '../utils/selector-types';

export type HomeSelectorMap = {
  header: Selector | Selector[];
  logout: Selector | Selector[];
};

export const HomeSelectors: HomeSelectorMap = {
  header: { kind: 'css', value: 'header h1' },
  logout: [{ kind: 'text', text: 'Log out' }, { kind: 'css', value: 'button#logout' }]
};
