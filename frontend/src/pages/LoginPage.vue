<template>
  <main class="page">
    <div class="panel">
      <h1 class="title">ファミリーTODOアプリ</h1>

      <form class="login-form" @submit.prevent="onSubmit">
        <div class="row">
          <label for="name">名前</label>
          <input
            id="name"
            v-model="form.name"
            type="text"
            autocomplete="username"
          />
        </div>

        <div class="row">
          <label for="password">パスワード</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            autocomplete="current-password"
          />
        </div>

        <div class="actions">
          <button type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? "送信中..." : "ログイン" }}
          </button>
        </div>

        <p v-if="message" class="message" :class="{ error: isError }">
          {{ message }}
        </p>
      </form>

      <nav class="links" aria-label="login-sub-actions">
        <RouterLink to="/family/register">家族追加</RouterLink>
      </nav>
    </div>
  </main>
</template>

<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const form = reactive({
  name: "",
  password: "",
});

const isSubmitting = ref(false);
const message = ref("");
const isError = ref(false);

const onSubmit = async () => {
  message.value = "";
  isError.value = false;
  isSubmitting.value = true;
  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || "";
    const response = await fetch(`${baseUrl}/auth/login/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: form.name,
        password: form.password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      if (data?.errors) {
        message.value = Object.entries(data.errors)
          .map(([key, value]) => `${key}: ${value}`)
          .join(" / ");
      } else {
        message.value = data?.error || "ログインに失敗しました。";
      }
      isError.value = true;
      return;
    }

    localStorage.setItem("loggedInFamilyName", data.name);
    await router.push("/todo/tasks");
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

.message {
  margin: 14px 0 0;
  font-size: 0.95rem;
  color: #1f2937;
}

.message.error {
  color: #b91c1c;
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
  opacity: 0.65;
  cursor: not-allowed;
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
