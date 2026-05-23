import { mount } from "@vue/test-utils";
import TaskCreatePage from "./TaskCreatePage.vue";

describe("TaskCreatePage", () => {
  it("新規作成フォームの骨組みを表示する", () => {
    const wrapper = mount(TaskCreatePage);

    expect(wrapper.get("[aria-label='task-create-view']").text()).toContain(
      "タスク新規作成",
    );
    expect(wrapper.get("[aria-label='task-create-form']").exists()).toBe(true);
    expect(wrapper.text()).toContain("戻る");
    expect(wrapper.text()).toContain("保存");
  });
});
