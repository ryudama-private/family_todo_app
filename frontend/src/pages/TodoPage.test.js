import { mount } from "@vue/test-utils";
import TodoPage from "./TodoPage.vue";

describe("TodoPage", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it("ログインユーザー名が未保存のときはデフォルト文言を表示する", () => {
    const wrapper = mount(TodoPage);

    expect(wrapper.get(".logged-in-user").text()).toContain("ログインしてる人");
  });

  it("ログインユーザー名が保存されているときはその名前を表示する", () => {
    localStorage.setItem("loggedInFamilyName", "お母さん");

    const wrapper = mount(TodoPage);

    expect(wrapper.get(".logged-in-user").text()).toContain("お母さん");
  });

  it("サイドバーのメニューを表示する", () => {
    const wrapper = mount(TodoPage);

    const navItems = wrapper.findAll(".nav").map((nav) => nav.text());
    expect(navItems).toContain("TODO 一覧");
    expect(navItems).toContain("カレンダー");
    expect(wrapper.get(".logout-btn").text()).toBe("ログアウト");
  });
});
