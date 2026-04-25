import { mount } from "@vue/test-utils";
import { nextTick } from "vue";
import FamilyRegisterPage from "./FamilyRegisterPage.vue";

const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0));

const RouterLinkStub = {
  props: ["to"],
  template: '<a :href="to"><slot /></a>',
};

describe("FamilyRegisterPage", () => {
  let wrapper;
  let originalFetch;

  beforeEach(() => {
    originalFetch = globalThis.fetch;
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({ name: "テスト太郎" }),
    });

    wrapper = mount(FamilyRegisterPage, {
      global: {
        stubs: {
          RouterLink: RouterLinkStub,
        },
      },
    });
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("家族登録フォームのタイトル、全項目、登録ボタンを表示する", () => {
    expect(wrapper.get(".title").text()).toBe("家族登録");
    expect(wrapper.get("#name").exists()).toBe(true);
    expect(wrapper.get("#password").attributes("type")).toBe("password");
    expect(wrapper.get("#secret-question").exists()).toBe(true);
    expect(wrapper.get("#secret-answer").exists()).toBe(true);
    expect(wrapper.get("button[type='submit']").text()).toBe("登録");
  });

  it("全項目を入力して登録ボタンを押して、登録が成功する", async () => {
    await wrapper.get("#name").setValue("テスト太郎");
    await wrapper.get("#password").setValue("password123");
    await wrapper.get("#secret-question").setValue("好きな食べ物は？");
    await wrapper.get("#secret-answer").setValue("カレー");

    expect(wrapper.get("#name").element.value).toBe("テスト太郎");
    expect(wrapper.get("#password").element.value).toBe("password123");
    expect(wrapper.get("#secret-question").element.value).toBe(
      "好きな食べ物は？",
    );
    expect(wrapper.get("#secret-answer").element.value).toBe("カレー");

    await wrapper.get("form").trigger("submit");
    await flushPromises();
    await nextTick();

    expect(globalThis.fetch).toHaveBeenCalledWith(
      "http://localhost:8000/auth/register/",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: "テスト太郎",
          password: "password123",
          secret_question: "好きな食べ物は？",
          secret_answer: "カレー",
        }),
      },
    );

    expect(wrapper.get(".message").text()).toBe("登録しました: テスト太郎");
  });

  it("登録失敗時にerrorsの内容を表示してエラースタイルになる", async () => {
    globalThis.fetch = vi.fn().mockResolvedValueOnce({
      ok: false,
      json: async () => ({
        errors: {
          name: "必須項目です。",
          password: "必須項目です。",
        },
      }),
    });

    await wrapper.get("form").trigger("submit");
    await flushPromises();
    await nextTick();

    const message = wrapper.get(".message");
    expect(message.text()).toContain("name: 必須項目です。");
    expect(message.text()).toContain("password: 必須項目です。");
    expect(message.classes()).toContain("error");
  });

  it("通信例外時に汎用エラーメッセージを表示してエラースタイルになる", async () => {
    globalThis.fetch = vi
      .fn()
      .mockRejectedValueOnce(new Error("network error"));

    await wrapper.get("form").trigger("submit");
    await flushPromises();
    await nextTick();

    const message = wrapper.get(".message");
    expect(message.text()).toBe("予期せぬエラーが発生しました。");
    expect(message.classes()).toContain("error");
  });
});
