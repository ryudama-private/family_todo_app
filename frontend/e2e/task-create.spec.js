import { expect, test } from "@playwright/test";

const cleanupToken = process.env.PW_E2E_CLEANUP_TOKEN || "local-test-token";

const createFamily = async (request, suffix) => {
  const registerResponse = await request.post("/auth/register/", {
    data: {
      name: `e2e-task-${suffix}`,
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

const cleanupTask = async (request, taskId) => {
  if (!taskId) {
    return;
  }

  const cleanupResponse = await request.delete(`/auth/todos/${taskId}/`);
  expect(cleanupResponse.ok()).toBeTruthy();
};

test.describe("Task create E2E", () => {
  test("タスク新規作成画面で入力して保存すると一覧に表示される", async ({
    page,
    request,
  }) => {
    let creatorFamilyId;
    let assigneeFamilyId;
    let createdTaskId;

    try {
      const creator = await createFamily(request, `${Date.now()}-creator`);
      const assignee = await createFamily(request, `${Date.now()}-assignee`);
      creatorFamilyId = creator.id;
      assigneeFamilyId = assignee.id;

      await page.addInitScript(
        ({ id, name }) => {
          localStorage.setItem("loggedInFamilyId", String(id));
          localStorage.setItem("loggedInFamilyName", name);
        },
        { id: creator.id, name: creator.name },
      );

      // ブラウザ側の /auth 呼び出しは実行環境で到達先が変わるため、
      // Playwright 経由で backend に中継する。
      await page.route("**/auth/families/", async (route) => {
        await route.fulfill({
          status: 200,
          contentType: "application/json",
          body: JSON.stringify({
            families: [
              { id: creator.id, name: creator.name },
              { id: assignee.id, name: assignee.name },
            ],
          }),
        });
      });

      await page.route("**/auth/todos/create/", async (route) => {
        const postData = route.request().postDataJSON();
        const backendResponse = await request.post("/auth/todos/create/", {
          data: postData,
        });
        const bodyText = await backendResponse.text();
        await route.fulfill({
          status: backendResponse.status(),
          contentType: "application/json",
          body: bodyText,
        });
      });

      await page.route("**/auth/todos/", async (route) => {
        const backendResponse = await request.get("/auth/todos/");
        const bodyText = await backendResponse.text();
        await route.fulfill({
          status: backendResponse.status(),
          contentType: "application/json",
          body: bodyText,
        });
      });

      await page.goto("/todo/tasks/create");
      await expect(page).toHaveURL(/\/todo\/tasks\/create$/);

      const title = `e2e-task-title-${Date.now()}`;

      await page.locator("label:has-text('やること') input").fill(title);
      await page
        .locator("label:has-text('やる人') select")
        .selectOption(String(assignee.id));

      const dueDateInput = page.locator("label:has-text('期限') .dp__input");
      await dueDateInput.click();
      await page
        .locator(".dp__calendar .dp__cell_inner")
        .filter({ hasNotText: /^$/ })
        .first()
        .click();
      await page.getByRole("button", { name: "Select" }).click();
      await expect(dueDateInput).not.toHaveValue("");

      await page
        .locator("label:has-text('進行状況') select")
        .selectOption("進行中");
      await page
        .locator("label:has-text('アラーム') select")
        .selectOption("none");

      const createResponsePromise = page.waitForResponse(
        "**/auth/todos/create/",
      );
      await page.getByRole("button", { name: "保存" }).click();
      const createResponse = await createResponsePromise;
      expect(createResponse.ok()).toBeTruthy();

      const createdTask = await createResponse.json();
      createdTaskId = createdTask.id;

      expect(createdTask.creator_id).toBe(creator.id);
      expect(createdTask.assignee_id).toBe(assignee.id);
      expect(createdTask.status).toBe("進行中");

      await expect(page).toHaveURL(/\/todo\/tasks$/);
      await expect(page.getByLabel("tasks-table")).toContainText(title);
    } finally {
      await cleanupTask(request, createdTaskId);
      await cleanupFamily(request, assigneeFamilyId);
      await cleanupFamily(request, creatorFamilyId);
    }
  });
});
