import { mount } from "@vue/test-utils";
import { reactive } from "vue";
import TopPage from "./TopPage.vue";

const replaceMock = vi.fn();
const pushMock = vi.fn();
const routeMock = reactive({ path: "/todo/tasks" });

vi.mock("vue-router", async () => {
  const actual = await vi.importActual("vue-router");
  return {
    ...actual,
    RouterView: {
      template: '<div class="router-view-stub" />',
    },
    useRoute: () => routeMock,
    useRouter: () => ({
      push: pushMock,
      replace: replaceMock,
    }),
  };
});

describe("TopPage", () => {
  const mountTopPage = () =>
    mount(TopPage, {
      global: {
        stubs: {
          RouterView: {
            template: '<div class="router-view-stub" />',
          },
        },
      },
    });

  beforeEach(() => {
    localStorage.clear();
    replaceMock.mockReset();
    pushMock.mockReset();
    routeMock.path = "/todo/tasks";
  });

  afterEach(() => {
    localStorage.clear();
  });

  it("ログインユーザー名が未保存のときはデフォルト文言を表示する", () => {
    const wrapper = mountTopPage();

    expect(wrapper.get(".logged-in-user").text()).toContain(
      "ログインしている人",
    );
  });

  it("ログインユーザー名が保存されているときはその名前を表示する", () => {
    localStorage.setItem("loggedInFamilyName", "お母さん");

    const wrapper = mountTopPage();

    expect(wrapper.get(".logged-in-user").text()).toContain("お母さん");
  });

  it("サイドバーのメニューを表示する", () => {
    const wrapper = mountTopPage();

    const navItems = wrapper.findAll(".nav").map((nav) => nav.text());
    expect(navItems).toContain("TODO 一覧");
    expect(navItems).toContain("カレンダー");
    expect(wrapper.get(".logout-btn").text()).toBe("ログアウト");
  });

  it("共通レイアウト内にRouterViewを表示する", () => {
    const wrapper = mountTopPage();

    expect(wrapper.get(".router-view-stub").exists()).toBe(true);
  });

  it("カレンダーボタン押下で /todo/calendar へ遷移する", async () => {
    const wrapper = mountTopPage();

    await wrapper.findAll(".nav")[1].trigger("click");

    expect(pushMock).toHaveBeenCalledWith("/todo/calendar");
  });
  it("ログアウト押下で保存済みユーザー名を削除し /login に遷移する（履歴置換）", async () => {
    localStorage.setItem("loggedInFamilyId", "1");
    localStorage.setItem("loggedInFamilyName", "お母さん");
    const wrapper = mountTopPage();

    await wrapper.get(".logout-btn").trigger("click");

    expect(localStorage.getItem("loggedInFamilyId")).toBeNull();
    expect(localStorage.getItem("loggedInFamilyName")).toBeNull();
    expect(replaceMock).toHaveBeenCalledWith("/login");
  });
});
