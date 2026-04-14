import { mount } from "@vue/test-utils";
import LoginPage from "./LoginPage.vue";

const RouterLinkStub = {
  props: ["to"],
  template: '<a :href="to"><slot /></a>',
};

describe("LoginPage", () => {
  let wrapper;

  beforeEach(() => {
    wrapper = mount(LoginPage, {
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    });
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

  it("名前とパスワードを入力してログインボタンを押せる", async () => {
    await wrapper.get("#name").setValue("テスト太郎");
    await wrapper.get("#password").setValue("password123");

    expect(wrapper.get("#name").element.value).toBe("テスト太郎");
    expect(wrapper.get("#password").element.value).toBe("password123");

    await wrapper.get("button[type='submit']").trigger("click");
  });
});
