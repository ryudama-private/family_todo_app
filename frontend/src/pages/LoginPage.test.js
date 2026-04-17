import { mount } from "@vue/test-utils";
import LoginPage from "./LoginPage.vue";

const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0));

const pushMock = vi.fn();

vi.mock("vue-router", async () => {
  const actual = await vi.importActual("vue-router");
  return {
    ...actual,
    useRouter: () => ({
      push: pushMock,
    }),
  };
});

const RouterLinkStub = {
  props: ["to"],
  template: '<a :href="to"><slot /></a>',
};

describe("LoginPage", () => {
  let wrapper;
  let originalFetch;

  beforeEach(() => {
    localStorage.clear();
    pushMock.mockReset();
    originalFetch = globalThis.fetch;
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ id: 1, name: "テスト太郎" }),
    });

    wrapper = mount(LoginPage, {
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    });
  });

  afterEach(() => {
    localStorage.clear();
    globalThis.fetch = originalFetch;
  });

  it("家族登録ページへのリンクを表示する", () => {
    const link = wrapper.get(".links a");
    expect(link.text()).toBe("家族追加");
    expect(link.attributes("href")).toBe("/family/register");
  });

  it("タイトル、名前とパスワードの入力欄、ログインボタンを表示する", () => {
    expect(wrapper.get(".title").text()).toBe("ファミリーTODOアプリ");
    expect(wrapper.get("#name").attributes("type")).toBe("text");
    expect(wrapper.get("#password").attributes("type")).toBe("password");
    expect(wrapper.get("button[type='submit']").text()).toBe("ログイン");
  });

  it("名前とパスワードを入力してログイン成功時に /todo へ遷移する", async () => {
    await wrapper.get("#name").setValue("テスト太郎");
    await wrapper.get("#password").setValue("password123");

    expect(wrapper.get("#name").element.value).toBe("テスト太郎");
    expect(wrapper.get("#password").element.value).toBe("password123");

    await wrapper.get("form").trigger("submit");
    await flushPromises();

    expect(globalThis.fetch).toHaveBeenCalledWith("/auth/login/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: "テスト太郎",
        password: "password123",
      }),
    });
    expect(localStorage.getItem("loggedInFamilyName")).toBe("テスト太郎");
    expect(pushMock).toHaveBeenCalledWith("/todo");
  });

  it("ログイン失敗時にエラーメッセージを表示する", async () => {
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      json: async () => ({
        error: "名前またはパスワードが違います。",
      }),
    });

    await wrapper.get("form").trigger("submit");
    await flushPromises();

    expect(wrapper.get(".message").text()).toBe(
      "名前またはパスワードが違います。",
    );
    expect(wrapper.get(".message").classes()).toContain("error");
    expect(pushMock).not.toHaveBeenCalled();
  });
});
