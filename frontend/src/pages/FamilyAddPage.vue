<template>
  <main class="stub-page">
    <div class="box">
      <h1>家族追加ページ</h1>
      <p>このページはこれから実装します。</p>
      <RouterLink to="/login">ログインへ戻る</RouterLink>
    </div>
  </main>
</template>

<style scoped>
.stub-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: #d7d7d7;
  font-family: "Yu Mincho", "Hiragino Mincho ProN", serif;
}

.box {
  width: min(560px, calc(100vw - 36px));
  border: 1px solid #595959;
  background: #ececec;
  padding: 28px;
}

h1 {
  margin: 0 0 12px;
  font-size: 1.7rem;
  font-weight: 400;
}

p {
  margin: 0 0 16px;
}

a {
  color: #1f2937;
}
</style>
