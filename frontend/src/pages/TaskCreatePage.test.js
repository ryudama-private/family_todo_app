import { mount } from "@vue/test-utils";
import { nextTick } from "vue";
import TaskCreatePage from "./TaskCreatePage.vue";

const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0));
const mountTaskCreatePage = () => mount(TaskCreatePage, { shallow: true });

describe("TaskCreatePage", () => {
  let originalFetch;

  beforeEach(() => {
    originalFetch = globalThis.fetch;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("新規作成フォームの骨組みを表示し、やる人プルダウンにfamily名を表示する", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        families: [
          { id: 1, name: "お母さん" },
          { id: 2, name: "お父さん" },
        ],
      }),
    });

    const wrapper = mountTaskCreatePage();
    await flushPromises();
    await nextTick();

    expect(wrapper.get("[aria-label='task-create-view']").text()).toContain(
      "タスク新規作成",
    );
    expect(wrapper.get("[aria-label='task-create-form']").exists()).toBe(true);
    expect(wrapper.text()).toContain("期限");
    expect(wrapper.text()).toContain("アラーム");
    expect(wrapper.findAll(".date-picker")).toHaveLength(1);
    expect(wrapper.text()).toContain("何分前にアラームをかけますか");
    expect(wrapper.text()).toContain("未設定");
    expect(wrapper.text()).toContain("30分前");
    expect(wrapper.text()).toContain("1時間前");
    expect(wrapper.text()).toContain("1日前");
    const options = wrapper
      .findAll("select option")
      .map((option) => option.text());
    expect(options).toContain("選択してください");
    expect(options).toContain("お母さん");
    expect(options).toContain("お父さん");
    expect(wrapper.text()).toContain("戻る");
    expect(wrapper.text()).toContain("保存");
  });

  it("family一覧の取得に失敗したときはエラー文言を表示する", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      json: async () => ({ error: "取得失敗" }),
    });

    const wrapper = mountTaskCreatePage();
    await flushPromises();
    await nextTick();

    expect(wrapper.text()).toContain("取得失敗");
  });

  it("進行状況は未対応・進行中・完了の3択から選べる", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ families: [] }),
    });

    const wrapper = mountTaskCreatePage();
    await flushPromises();
    await nextTick();

    const statusSelect = wrapper.findAll("select")[1];
    const statusOptions = statusSelect.findAll("option").map((o) => o.text());

    expect(statusOptions).toEqual(["未対応", "進行中", "完了"]);
  });
});
