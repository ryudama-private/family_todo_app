import { mount } from "@vue/test-utils";
import TodoPage from "./TodoPage.vue";

const replaceMock = vi.fn();

vi.mock("vue-router", async () => {
  const actual = await vi.importActual("vue-router");
  return {
    ...actual,
    useRouter: () => ({
      replace: replaceMock,
    }),
  };
});

describe("TodoPage", () => {
  beforeEach(() => {
    localStorage.clear();
    replaceMock.mockReset();
  });

  afterEach(() => {
    localStorage.clear();
  });

  it("ログインユーザー名が未保存のときはデフォルト文言を表示する", () => {
    const wrapper = mount(TodoPage);

    expect(wrapper.get(".logged-in-user").text()).toContain(
      "ログインしている人",
    );
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

  it("ログアウト押下で保存済みユーザー名を削除し /login に遷移する（履歴置換）", async () => {
    localStorage.setItem("loggedInFamilyName", "お母さん");
    const wrapper = mount(TodoPage);

    await wrapper.get(".logout-btn").trigger("click");

    expect(localStorage.getItem("loggedInFamilyName")).toBeNull();
    expect(replaceMock).toHaveBeenCalledWith("/login");
  });
});
