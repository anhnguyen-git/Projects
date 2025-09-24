import { test, expect } from '../fixtures/test-fixtures';

test.describe('smoke: public flows', () => {
  test('login should succeed with valid credentials', async ({ loginPage, homePage, page }) => {
    await loginPage.goto();
    await loginPage.login('demo@example.com', 'Password123');

    await page.waitForURL('**/home');
    expect(await homePage.getHeaderText()).toContain('Welcome');
  });
});
