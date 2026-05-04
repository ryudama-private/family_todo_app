import { expect, test } from "@playwright/test";

const cleanupToken = process.env.PW_E2E_CLEANUP_TOKEN || "local-test-token";

const createFamily = async (request, suffix) => {
  const registerResponse = await request.post("/auth/register/", {
    data: {
      name: `e2e-login-${suffix}`,
      password: "password123",
      secret_question: "好きな食べ物は？",
      secret_answer: "カレー",
    },
  });

  expect(registerResponse.ok()).toBeTruthy();
  const payload = await registerResponse.json();
  return {
    id: payload.id,
    name: payload.name,
    password: "password123",
  };
};

const cleanupFamily = async (request, familyId) => {
  if (!familyId) {
    return;
  }

  expect(cleanupToken).toBeTruthy();

  const cleanupResponse = await request.delete(`/auth/register/${familyId}/`, {
    headers: {
      "X-E2E-Cleanup-Token": cleanupToken,
    },
  });
  expect(cleanupResponse.ok()).toBeTruthy();
};

test.describe("Login E2E", () => {
  test("正しい認証情報でログインすると /todo/tasks に遷移する", async ({
    page,
    request,
  }) => {
    let createdFamilyId;

    try {
      const family = await createFamily(request, Date.now());
      createdFamilyId = family.id;

      await page.goto("/login");
      await page.getByLabel("名前").fill(family.name);
      await page.getByLabel("パスワード").fill(family.password);
      await page.getByRole("button", { name: "ログイン" }).click();

      await expect(page).toHaveURL(/\/todo\/tasks$/);
      await expect(page.getByLabel("todo-layout")).toBeVisible();
      await expect(
        page
          .getByLabel("tasks-view")
          .getByRole("heading", { name: "TODO 一覧" }),
      ).toBeVisible();
    } finally {
      await cleanupFamily(request, createdFamilyId);
    }
  });

  test("ログイン後に /todo/tasks でログイン中ユーザー名が表示される", async ({
    page,
    request,
  }) => {
    let createdFamilyId;

    try {
      const family = await createFamily(request, `${Date.now()}-name`);
      createdFamilyId = family.id;

      await page.goto("/login");
      await page.getByLabel("名前").fill(family.name);
      await page.getByLabel("パスワード").fill(family.password);
      await page.getByRole("button", { name: "ログイン" }).click();

      await expect(page).toHaveURL(/\/todo\/tasks$/);
      await expect(page.locator(".logged-in-user")).toContainText(family.name);
    } finally {
      await cleanupFamily(request, createdFamilyId);
    }
  });

  test("/todo/tasks でログアウトすると /login に戻り保持していた name が削除される", async ({
    page,
    request,
  }) => {
    let createdFamilyId;

    try {
      const family = await createFamily(request, `${Date.now()}-logout`);
      createdFamilyId = family.id;

      await page.goto("/login");
      await page.getByLabel("名前").fill(family.name);
      await page.getByLabel("パスワード").fill(family.password);
      await page.getByRole("button", { name: "ログイン" }).click();

      await expect(page).toHaveURL(/\/todo\/tasks$/);
      await page.getByRole("button", { name: "ログアウト" }).click();

      await expect(page).toHaveURL(/\/login$/);

      const storedName = await page.evaluate(() =>
        localStorage.getItem("loggedInFamilyName"),
      );
      expect(storedName).toBeNull();
    } finally {
      await cleanupFamily(request, createdFamilyId);
    }
  });

  test("誤ったパスワードではログインできずエラーメッセージが表示される", async ({
    page,
    request,
  }) => {
    let createdFamilyId;

    try {
      const family = await createFamily(request, `${Date.now()}-invalid`);
      createdFamilyId = family.id;

      await page.goto("/login");
      await page.getByLabel("名前").fill(family.name);
      await page.getByLabel("パスワード").fill("wrong-password");
      await page.getByRole("button", { name: "ログイン" }).click();

      await expect(page).toHaveURL(/\/login$/);
      await expect(page.locator(".message.error")).toContainText(
        "名前またはパスワードが違います。",
      );
    } finally {
      await cleanupFamily(request, createdFamilyId);
    }
  });

  test("ログアウト後にブラウザの戻るボタンで /todo/tasks に戻れない（履歴置換により保護）", async ({
    page,
    request,
  }) => {
    let createdFamilyId;

    try {
      const family = await createFamily(
        request,
        `${Date.now()}-back-protection`,
      );
      createdFamilyId = family.id;

      // ログイン
      await page.goto("/login");
      await page.getByLabel("名前").fill(family.name);
      await page.getByLabel("パスワード").fill(family.password);
      await page.getByRole("button", { name: "ログイン" }).click();

      await expect(page).toHaveURL(/\/todo\/tasks$/);

      // ログアウト
      await page.getByRole("button", { name: "ログアウト" }).click();
      await expect(page).toHaveURL(/\/login$/);

      // ブラウザの戻るボタンを押す
      await page.goBack();

      // /login に留まっていることを確認（/todo/tasks に戻らない）
      await expect(page).toHaveURL(/\/login$/);
    } finally {
      await cleanupFamily(request, createdFamilyId);
    }
  });
});
