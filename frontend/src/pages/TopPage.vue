<template>
  <main class="page">
    <section class="frame" aria-label="todo-layout">
      <aside class="side" aria-label="todo-navigation">
        <div class="logged-in-user">
          <div>ログインしている人</div>
          <span class="line">{{ loggedInName }}</span>
        </div>

        <nav class="menu" aria-label="todo-menu">
          <button
            type="button"
            class="nav"
            :class="{ active: route.path.startsWith('/todo/tasks') }"
            @click="goToTasks"
          >
            TODO 一覧
          </button>
          <button
            type="button"
            class="nav"
            :class="{ active: route.path === '/todo/calendar' }"
            @click="goToCalendar"
          >
            カレンダー
          </button>
        </nav>

        <button type="button" class="logout-btn" @click="onLogout">
          ログアウト
        </button>
      </aside>

      <section class="content" aria-label="todo-content">
        <RouterView />
      </section>
    </section>
  </main>
</template>

<script setup>
import { ref } from "vue";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute();

const loggedInName = ref(
  localStorage.getItem("loggedInFamilyName") || "ログインしている人",
);

const goToTasks = async () => {
  if (route.path !== "/todo/tasks") {
    await router.push("/todo/tasks");
  }
};

const goToCalendar = async () => {
  if (route.path !== "/todo/calendar") {
    await router.push("/todo/calendar");
  }
};

const onLogout = async () => {
  localStorage.removeItem("loggedInFamilyName");
  await router.replace("/login");
};
</script>

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

.logged-in-user {
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
  border: none;
  background: transparent;
  font-size: 0.75rem;
  letter-spacing: 0.03em;
  font-family: inherit;
  cursor: pointer;
}

.logout-btn {
  display: grid;
  place-items: center;
  height: 34px;
  font-size: 0.75rem;
  letter-spacing: 0.03em;
  margin-top: auto;
  cursor: pointer;
}

.content {
  padding: 28px 32px;
  background: linear-gradient(180deg, #fcfdff 0%, #f4f7fb 100%);
}

.nav.active {
  background: #dbe7ff;
  font-weight: 700;
}

.nav:hover,
.logout-btn:hover {
  background: #edf1ff;
}
</style>
