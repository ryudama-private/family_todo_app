import router from "./index";

describe("router", () => {
  it("ログインと家族登録のルートを持つ", () => {
    const paths = router.getRoutes().map((route) => route.path);

    expect(paths).toContain("/");
    expect(paths).toContain("/login");
    expect(paths).toContain("/family/register");
  });

  it("/ から /login へリダイレクトする設定を持つ", () => {
    const rootRoute = router.getRoutes().find((route) => route.path === "/");

    expect(rootRoute).toBeDefined();
    expect(rootRoute.redirect).toBe("/login");
  });

  it("todo配下にtasksとcalendarのルートを持つ", () => {
    const paths = router.getRoutes().map((route) => route.path);

    expect(paths).toContain("/todo");
    expect(paths).toContain("/todo/tasks");
    expect(paths).toContain("/todo/calendar");
  });
});
