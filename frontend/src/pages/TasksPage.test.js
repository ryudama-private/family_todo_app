import { mount } from "@vue/test-utils";
import TasksPage from "./TasksPage.vue";

describe("TasksPage", () => {
  it("TODO一覧の見出しと説明を表示する", () => {
    const wrapper = mount(TasksPage);

    expect(wrapper.get("[aria-label='tasks-view']").text()).toContain(
      "TODO 一覧",
    );
    expect(wrapper.text()).toContain("登録されたタスクをここに表示します。");
  });
});
