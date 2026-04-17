import { mount } from "@vue/test-utils";
import TodoPage from "./TodoPage.vue";

describe("TodoPage", () => {
  it("サイドバーのメニューを表示する", () => {
    const wrapper = mount(TodoPage);

    expect(wrapper.get(".logged-in-user").text()).toContain("ログインしてる人");

    const navItems = wrapper.findAll(".nav").map((nav) => nav.text());
    expect(navItems).toContain("TODO 一覧");
    expect(navItems).toContain("カレンダー");
    expect(wrapper.get(".logout-btn").text()).toBe("ログアウト");
  });
});
