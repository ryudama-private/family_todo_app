<template>
  <main class="page">
    <div class="panel">
      <!-- <h1 class="title">家族登録</h1> -->
      <h1 class="title">CICDテスト1回目</h1>

      <form class="add-form" @submit.prevent="onSubmit">
        <div class="row">
          <label for="name">名前</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            autocomplete="name"
          />
        </div>

        <div class="row">
          <label for="password">パスワード</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            autocomplete="new-password"
          />
        </div>

        <div class="row">
          <label for="secret-question">秘密の質問</label>
          <input
            id="secret-question"
            v-model="form.secretQuestion"
            type="text"
          />
        </div>

        <div class="row">
          <label for="secret-answer">秘密の回答</label>
          <input id="secret-answer" v-model="form.secretAnswer" type="text" />
        </div>

        <div class="actions">
          <button type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? "送信中..." : "登録" }}
          </button>
        </div>

        <p v-if="message" class="message" :class="{ error: isError }">
          {{ message }}
        </p>
      </form>

      <nav class="links" aria-label="family-register-sub-actions">
        <RouterLink to="/login">ログインページへ戻る</RouterLink>
      </nav>
    </div>
  </main>
</template>

<script setup>
import { reactive, ref } from "vue";

const form = reactive({
  name: "",
  password: "",
  secretQuestion: "",
  secretAnswer: "",
});

const isSubmitting = ref(false);
const message = ref("");
const isError = ref(false);

const resetForm = () => {
  form.name = "";
  form.password = "";
  form.secretQuestion = "";
  form.secretAnswer = "";
};

const onSubmit = async () => {
  message.value = "";
  isError.value = false;
  isSubmitting.value = true;

  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || "";
    const response = await fetch(`${baseUrl}/auth/register/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: form.name,
        password: form.password,
        secret_question: form.secretQuestion,
        secret_answer: form.secretAnswer,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      if (data?.errors) {
        message.value = Object.entries(data.errors)
          .map(([key, value]) => `${key}: ${value}`)
          .join(" / ");
      } else {
        message.value = data?.error || "登録に失敗しました。";
      }
      isError.value = true;
      return;
    }

    message.value = `登録しました: ${data.name}`;
    resetForm();
  } catch {
    message.value = "予期せぬエラーが発生しました。";
    isError.value = true;
  } finally {
    isSubmitting.value = false;
  }
};
</script>

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

.message {
  margin-top: 12px;
  font-size: 0.95rem;
  color: #1f7a1f;
  font-family: "Yu Gothic", "Hiragino Kaku Gothic ProN", sans-serif;
}

.message.error {
  color: #b42318;
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

button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
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
