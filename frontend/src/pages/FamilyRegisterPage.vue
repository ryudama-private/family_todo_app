<template>
  <main class="page">
    <div class="panel">
      <h1 class="title">家族登録</h1>

      <form class="add-form" @submit.prevent>
        <div class="row">
          <label for="name">名前</label>
          <input id="name" type="text" autocomplete="name" />
        </div>

        <div class="row">
          <label for="password">パスワード</label>
          <input id="password" type="password" autocomplete="new-password" />
        </div>

        <div class="row">
          <label for="secret-question">秘密の質問</label>
          <input id="secret-question" type="text" />
        </div>

        <div class="row">
          <label for="secret-answer">秘密の回答</label>
          <input id="secret-answer" type="text" />
        </div>

        <div class="actions">
          <button type="submit">登録</button>
        </div>
      </form>

      <nav class="links" aria-label="family-register-sub-actions">
        <RouterLink to="/login">ログインページへ戻る</RouterLink>
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

.add-form {
  width: min(580px, 100%);
  margin: 220px auto 0;
}

.row {
  display: grid;
  grid-template-columns: 170px 1fr;
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
  font-size: 1.2rem;
  padding: 0 14px;
  font-family: "Yu Gothic", "Hiragino Kaku Gothic ProN", sans-serif;
}

.actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 24px;
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
  text-align: right;
}

.links a {
  color: #2e2e2e;
  text-decoration: none;
  font-size: 1.4rem;
}

.links a:hover {
  color: #2563eb;
  text-decoration: underline;
}
</style>
