import { expect, test } from "@playwright/test";

test.describe("Family register E2E", () => {
  test("家族登録画面で入力して登録できる", async ({ page }) => {
    await page.goto("/family/register");

    await page.getByLabel("名前").fill(`e2e-user-${Date.now()}`);
    await page.getByLabel("パスワード").fill("password123");
    await page.getByLabel("秘密の質問").fill("好きな食べ物は？");
    await page.getByLabel("秘密の回答").fill("カレー");

    await page.getByRole("button", { name: "登録" }).click();

    await expect(page.locator(".message")).toContainText("登録しました:");
  });
});
