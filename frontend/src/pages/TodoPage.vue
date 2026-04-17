<template>
  <main class="page">
    <section class="frame" aria-label="todo-layout">
      <aside class="side" aria-label="todo-navigation">
        <p class="logined-user">
          <span class="line">ログインしてる人</span>
        </p>

        <nav class="menu" aria-label="todo-menu">
          <span class="nav">TODO 一覧</span>
          <span class="nav">カレンダー</span>
        </nav>

        <button type="button" class="logout-btn">ログアウト</button>
      </aside>

      <section class="content" aria-label="todo-content" />
    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  padding: 18px;
  box-sizing: border-box;
  font-family: "Yu Gothic", "Hiragino Kaku Gothic ProN", sans-serif;
}

.frame {
  width: min(980px, 100%);
  min-height: min(700px, calc(100vh - 36px));
  border: 2px solid black;
  display: grid;
  grid-template-columns: 170px 1fr;
}

.side {
  border-right: 2px solid black;
  padding: 18px 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.logined-user {
  margin: 0;
  padding: 10px 8px;
  font-size: 0.75rem;
  line-height: 1.4;
  letter-spacing: 0.02em;
  text-align: center;
}

.menu {
  display: grid;
  gap: 14px;
}

.nav {
  display: grid;
  place-items: center;
  height: 34px;
  font-size: 0.75rem;
  letter-spacing: 0.03em;
  cursor: pointer;
}

.logout-btn {
  display: grid;
  place-items: center;
  height: 34px;
  font-size: 0.75rem;
  letter-spacing: 0.03em;
}

.nav:hover,
.logout-btn:hover {
  background: #edf1ff;
}

.logout-btn {
  margin-top: auto;
  cursor: pointer;
}
</style>
