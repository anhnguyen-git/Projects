import { test, expect } from '../fixtures/test-fixtures';

test('login fails with wrong password', async ({ loginPage, page }) => {
  await loginPage.goto();
  await loginPage.login('demo@example.com', 'badpassword');
  await expect(page.locator('.alert-error')).toBeVisible();
});
