import BasePage from './base.page';
import { HomeSelectors } from './home.selectors';

export default class HomePage extends BasePage {
  constructor(page: any) {
    super(page);
  }

  async goto() {
    await this.page.goto('/');
  }

  async getHeaderText(): Promise<string | null> {
    return this.getText(HomeSelectors.header);
  }

  async logout() {
    await this.click(HomeSelectors.logout);
  }
}
