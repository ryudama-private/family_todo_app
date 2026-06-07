import { expect, test } from "@playwright/test";

const cleanupToken = process.env.PW_E2E_CLEANUP_TOKEN || "local-test-token";

const createFamily = async (request, suffix) => {
  const registerResponse = await request.post("/auth/register/", {
    data: {
      name: `e2e-task-delete-${suffix}`,
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
  };
};

const createTask = async (request, { title, creatorId, assigneeId }) => {
  const dueDate = new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString();
  const createResponse = await request.post("/auth/todos/create/", {
    data: {
      title,
      creator_id: creatorId,
      assignee_id: assigneeId,
      due_date: dueDate,
      status: "未対応",
      alarm_minutes: null,
    },
  });

  expect(createResponse.ok()).toBeTruthy();
  return createResponse.json();
};

const cleanupTask = async (request, taskId) => {
  if (!taskId) {
    return;
  }

  const cleanupResponse = await request.delete(`/auth/todos/${taskId}/`);
  expect(cleanupResponse.ok()).toBeTruthy();
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

test.describe("Task delete E2E", () => {
  test("TODO一覧の削除ボタンを押すと対象タスクが削除される", async ({
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

      const title = `e2e-task-delete-${Date.now()}`;
      const task = await createTask(request, {
        title,
        creatorId: creator.id,
        assigneeId: assignee.id,
      });
      createdTaskId = task.id;

      await page.addInitScript(
        ({ id, name }) => {
          localStorage.setItem("loggedInFamilyId", String(id));
          localStorage.setItem("loggedInFamilyName", name);
        },
        { id: creator.id, name: creator.name },
      );

      await page.route("**/auth/todos/", async (route) => {
        const backendResponse = await request.get("/auth/todos/");
        const bodyText = await backendResponse.text();
        await route.fulfill({
          status: backendResponse.status(),
          contentType: "application/json",
          body: bodyText,
        });
      });

      await page.route(`**/auth/todos/${createdTaskId}/`, async (route) => {
        const backendResponse = await request.delete(
          `/auth/todos/${createdTaskId}/`,
        );
        const bodyText = await backendResponse.text();
        await route.fulfill({
          status: backendResponse.status(),
          contentType: "application/json",
          body: bodyText,
        });
      });

      await page.goto("/todo/tasks");
      await expect(page).toHaveURL(/\/todo\/tasks$/);

      const targetRow = page.locator("tbody tr", { hasText: title });
      await expect(targetRow).toBeVisible();

      const deleteResponsePromise = page.waitForResponse(
        `**/auth/todos/${createdTaskId}/`,
      );
      await targetRow.getByRole("button", { name: "削除" }).click();
      const deleteResponse = await deleteResponsePromise;

      expect(deleteResponse.ok()).toBeTruthy();
      const deletePayload = await deleteResponse.json();
      expect(deletePayload.deleted_id).toBe(createdTaskId);

      createdTaskId = undefined;
      await expect(page.locator("tbody tr", { hasText: title })).toHaveCount(0);
    } finally {
      await cleanupTask(request, createdTaskId);
      await cleanupFamily(request, assigneeFamilyId);
      await cleanupFamily(request, creatorFamilyId);
    }
  });
});
