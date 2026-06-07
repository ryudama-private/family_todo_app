import { mount } from "@vue/test-utils";
import { nextTick } from "vue";
import TasksPage from "./TasksPage.vue";

const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0));
const mountTasksPage = () =>
  mount(TasksPage, {
    global: {
      stubs: {
        RouterLink: {
          props: ["to"],
          template: '<a :href="to"><slot /></a>',
        },
      },
    },
  });

describe("TasksPage", () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = globalThis.fetch;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("TODO一覧の見出しと取得したタスク表を表示する", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        tasks: [
          {
            id: 1,
            title: "ゴミ捨て",
            creator_id: 1,
            creator_name: "お母さん",
            assignee_id: 1,
            assignee_name: "お母さん",
            due_date: "2026-07-15T07:00:00Z",
            status: "未対応",
            alarm_minutes: 30,
          },
        ],
      }),
    });

    const wrapper = mountTasksPage();
    await flushPromises();
    await nextTick();

    expect(wrapper.get("[aria-label='tasks-view']").text()).toContain(
      "TODO 一覧",
    );
    expect(wrapper.get("[aria-label='tasks-table']").text()).toContain(
      "ゴミ捨て",
    );
    expect(wrapper.text()).toContain("お母さん");
    expect(wrapper.text()).toContain("未対応");
    expect(wrapper.text()).toContain("30分前");
    expect(wrapper.text()).toContain("削除");
  });

  it("取得失敗時にエラーメッセージを表示する", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ error: "取得失敗" }),
    });

    const wrapper = mountTasksPage();
    await flushPromises();
    await nextTick();

    expect(wrapper.text()).toContain("取得失敗");
  });

  it("削除ボタン押下でDELETE APIを呼び出し、対象行を一覧から消す", async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          tasks: [
            {
              id: 1,
              title: "ゴミ捨て",
              creator_id: 1,
              creator_name: "お母さん",
              assignee_id: 1,
              assignee_name: "お母さん",
              due_date: "2026-07-15T07:00:00Z",
              status: "未対応",
              alarm_minutes: 30,
            },
            {
              id: 2,
              title: "買い物",
              creator_id: 1,
              creator_name: "お母さん",
              assignee_id: 2,
              assignee_name: "お父さん",
              due_date: "2026-07-16T07:00:00Z",
              status: "進行中",
              alarm_minutes: null,
            },
          ],
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        json: async () => ({ deleted_id: 1 }),
      });

    const wrapper = mountTasksPage();
    await flushPromises();
    await nextTick();

    const firstDeleteButton = wrapper.findAll(".delete-btn")[0];
    await firstDeleteButton.trigger("click");
    await flushPromises();
    await nextTick();

    expect(globalThis.fetch).toHaveBeenNthCalledWith(
      2,
      expect.stringMatching(/\/auth\/todos\/1\/$/),
      {
        method: "DELETE",
      },
    );
    expect(wrapper.text()).not.toContain("ゴミ捨て");
    expect(wrapper.text()).toContain("買い物");
  });
});
