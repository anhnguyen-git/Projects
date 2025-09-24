import { test as base } from '@playwright/test';
import LoginPage from '../pages/login.page';
import HomePage from '../pages/home.page';

type MyFixtures = {
  loginPage: LoginPage;
  homePage: HomePage;
};

export const test = base.extend<MyFixtures>({
  loginPage: async ({ page }, use) => {
    await use(new LoginPage(page));
  },
  homePage: async ({ page }, use) => {
    await use(new HomePage(page));
  }
});

export { expect } from '@playwright/test';
