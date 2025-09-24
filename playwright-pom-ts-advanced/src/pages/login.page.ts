import BasePage from './base.page';
import type { Page } from '@playwright/test';
import { LoginSelectors, userRowFactory } from './login.selectors';

export default class LoginPage extends BasePage {
  constructor(page: Page) {
    super(page);
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.fill(LoginSelectors.username, username);
    await this.fill(LoginSelectors.password, password);
    await this.click(LoginSelectors.submit);
  }

  async getError(): Promise<string | null> {
    return this.getText(LoginSelectors.error);
  }

  async isUserRowPresent(username: string) {
    return this.isVisible(() => userRowFactory(username));
  }

  async userRowLocator(username: string) {
    return this.locator(() => userRowFactory(username));
  }
}
