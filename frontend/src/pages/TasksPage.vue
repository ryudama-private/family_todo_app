<template>
  <section class="panel" aria-label="tasks-view">
    <h1 class="panel-title">TODO 一覧</h1>

    <p v-if="isLoading" class="panel-copy">読み込み中...</p>
    <p v-else-if="errorMessage" class="panel-copy error">{{ errorMessage }}</p>

    <div v-else class="table-wrap">
      <table class="tasks-table" aria-label="tasks-table">
        <thead>
          <tr>
            <th>やること</th>
            <th>作った人</th>
            <th>やる人</th>
            <th>期限</th>
            <th>進行状況</th>
            <th>アラーム</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="tasks.length === 0">
            <td colspan="6" class="empty">タスクがありません</td>
          </tr>
          <tr v-for="task in tasks" :key="task.id">
            <td>{{ task.title }}</td>
            <td>{{ task.creator_name || `ID:${task.creator_id}` }}</td>
            <td>{{ task.assignee_name || `ID:${task.assignee_id}` }}</td>
            <td>{{ formatDueDate(task.due_date) }}</td>
            <td>{{ task.status }}</td>
            <td>{{ formatAlarm(task.alarm_minutes) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";

const tasks = ref([]);
const isLoading = ref(true);
const errorMessage = ref("");

const loadTasks = async () => {
  isLoading.value = true;
  errorMessage.value = "";
  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || "";
    const response = await fetch(`${baseUrl}/auth/todos/`);
    const data = await response.json();
    if (!response.ok) {
      errorMessage.value = data?.error || "タスクの取得に失敗しました。";
      tasks.value = [];
      return;
    }
    tasks.value = Array.isArray(data?.tasks) ? data.tasks : [];
  } catch {
    errorMessage.value = "タスクの取得に失敗しました。";
    tasks.value = [];
  } finally {
    isLoading.value = false;
  }
};

const formatDueDate = (value) => {
  if (!value) return "-";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  const month = date.getMonth() + 1;
  const day = date.getDate();
  const hour = date.getHours();
  const minute = String(date.getMinutes()).padStart(2, "0");
  return `${month}/${day} ${hour}:${minute}`;
};

const formatAlarm = (value) => {
  if (!Number.isFinite(value)) return "-";
  if (value % 1440 === 0) {
    return `${value / 1440}日前`;
  }
  return `${value}分前`;
};

onMounted(loadTasks);
</script>

<style scoped>
.panel {
  min-height: 100%;
  padding: 28px;
  box-sizing: border-box;
}

.panel-title {
  margin: 0 0 14px;
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: 0.04em;
}

.panel-copy {
  margin: 0;
  color: #374151;
  line-height: 1.7;
}

.panel-copy.error {
  color: #b91c1c;
}

.table-wrap {
  margin-top: 16px;
  overflow-x: auto;
}

.tasks-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  font-size: 0.95rem;
}

.tasks-table th,
.tasks-table td {
  border: 1px solid #9ca3af;
  padding: 10px 8px;
  text-align: left;
  vertical-align: middle;
}

.tasks-table th {
  background: #e5e7eb;
  font-weight: 700;
}

.empty {
  text-align: center;
  color: #6b7280;
}
</style>
