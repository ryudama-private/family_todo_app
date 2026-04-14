<template>
  <main class="page">
    <div class="panel">
      <h1 class="title">ファミリーTODOアプリ</h1>

      <form class="login-form" @submit.prevent>
        <div class="row">
          <label for="name">名前</label>
          <input id="name" type="text" autocomplete="username" />
        </div>

        <div class="row">
          <label for="password">パスワード</label>
          <input
            id="password"
            type="password"
            autocomplete="current-password"
          />
        </div>

        <div class="actions">
          <button type="submit">ログイン</button>
        </div>
      </form>

      <nav class="links" aria-label="login-sub-actions">
        <RouterLink to="/family/register">家族追加</RouterLink>
      </nav>
    </div>
  </main>
</template>

<style scoped>
.page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  font-family: "Yu Mincho", "Hiragino Mincho ProN", serif;
}

.panel {
  width: min(760px, calc(100vw - 48px));
  min-height: min(880px, calc(100vh - 40px));
  border: 1px solid #595959;
  position: relative;
  padding: 96px 64px 72px;
  box-sizing: border-box;
}

.title {
  text-align: center;
  font-size: clamp(2rem, 3vw, 2.4rem);
  font-weight: 400;
  margin: 0;
  letter-spacing: 0.04em;
}

.login-form {
  width: min(460px, 100%);
  margin: 380px auto 0;
}

.row {
  display: grid;
  grid-template-columns: 160px 1fr;
  align-items: center;
  margin-bottom: 20px;
  column-gap: 18px;
}

label {
  font-size: 2rem;
  text-align: right;
  line-height: 1;
}

input {
  height: 54px;
  border: 1px solid #555;
  background: transparent;
  font-size: 1.3rem;
  padding: 0 14px;
  font-family: "Yu Gothic", "Hiragino Kaku Gothic ProN", sans-serif;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

button {
  border: 1px solid #555;
  background: #e4e4e4;
  min-width: 112px;
  height: 56px;
  font-size: 1.6rem;
  font-family: "Yu Mincho", "Hiragino Mincho ProN", serif;
  cursor: pointer;
}

button:hover {
  background: #dadada;
}

.links {
  position: absolute;
  right: 28px;
  bottom: 34px;
  display: grid;
  gap: 10px;
  text-align: right;
}

.links a {
  color: #2e2e2e;
  text-decoration: none;
  font-size: 1.95rem;
  line-height: 1.1;
}

.links a:hover {
  color: #2563eb;
  text-decoration: underline;
}
</style>
