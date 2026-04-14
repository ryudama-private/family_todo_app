import { expect, test } from "@playwright/test";

test.describe("Family register E2E", () => {
  test("家族登録画面で入力して登録できる", async ({ page, request }) => {
    let createdFamilyId;

    try {
      await page.goto("/family/register");

      await page.getByLabel("名前").fill(`e2e-user-${Date.now()}`);
      await page.getByLabel("パスワード").fill("password123");
      await page.getByLabel("秘密の質問").fill("好きな食べ物は？");
      await page.getByLabel("秘密の回答").fill("カレー");

      const registerResponsePromise = page.waitForResponse("**/auth/register/");
      await page.getByRole("button", { name: "登録" }).click();
      const registerResponse = await registerResponsePromise;
      const payload = await registerResponse.json();
      createdFamilyId = payload.id;

      await expect(page.locator(".message")).toContainText("登録しました:");
    } finally {
      if (createdFamilyId) {
        const cleanupResponse = await request.delete(
          `/auth/register/${createdFamilyId}/`,
        );
        expect(cleanupResponse.ok()).toBeTruthy();
      }
    }
  });
});
