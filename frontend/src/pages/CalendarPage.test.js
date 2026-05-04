import { mount } from "@vue/test-utils";
import CalendarPage from "./CalendarPage.vue";

describe("CalendarPage", () => {
  it("カレンダーの見出しと説明を表示する", () => {
    const wrapper = mount(CalendarPage);

    expect(wrapper.get("[aria-label='calendar-view']").text()).toContain(
      "カレンダー",
    );
    expect(wrapper.text()).toContain(
      "タスクの予定をカレンダーで確認できます。",
    );
  });
});
