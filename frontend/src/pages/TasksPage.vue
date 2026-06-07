<template>
  <section class="panel" aria-label="tasks-view">
    <h1 class="panel-title">TODO 一覧</h1>

    <p v-if="isLoading" class="panel-copy">読み込み中...</p>
    <p v-else-if="errorMessage" class="panel-copy error">{{ errorMessage }}</p>

    <div v-else class="table-wrap">
      <div class="table-actions">
        <RouterLink class="create-label" to="/todo/tasks/create"
          >+新規作成</RouterLink
        >
      </div>
      <table class="tasks-table" aria-label="tasks-table">
        <thead>
          <tr>
            <th>やること</th>
            <th>作った人</th>
            <th>やる人</th>
            <th>期限</th>
            <th>進行状況</th>
            <th>アラーム</th>
            <th class="action-head" aria-label="操作"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="tasks.length === 0">
            <td colspan="7" class="empty">タスクがありません</td>
          </tr>
          <tr v-for="task in tasks" :key="task.id">
            <td>{{ task.title }}</td>
            <td>{{ task.creator_name || `ID:${task.creator_id}` }}</td>
            <td>{{ task.assignee_name || `ID:${task.assignee_id}` }}</td>
            <td>{{ formatDueDate(task.due_date) }}</td>
            <td>{{ task.status }}</td>
            <td>{{ formatAlarm(task.alarm_minutes) }}</td>
            <td class="action-cell">
              <button
                type="button"
                class="delete-btn"
                :disabled="deletingTaskId !== null"
                @click="deleteTask(task.id)"
              >
                削除
              </button>
            </td>
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
const deletingTaskId = ref(null);

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

const deleteTask = async (taskId) => {
  if (deletingTaskId.value !== null) return;

  deletingTaskId.value = taskId;
  errorMessage.value = "";

  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || "";
    const response = await fetch(`${baseUrl}/auth/todos/${taskId}/`, {
      method: "DELETE",
    });
    const data = await response.json();

    if (!response.ok) {
      errorMessage.value = data?.error || "タスクの削除に失敗しました。";
      return;
    }

    tasks.value = tasks.value.filter((task) => task.id !== taskId);
  } catch {
    errorMessage.value = "タスクの削除に失敗しました。";
  } finally {
    deletingTaskId.value = null;
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
  if (value === 0) return "期限切れ";
  if (value % 1440 === 0) return `${value / 1440}日前`;
  if (value >= 60) return `${Math.floor(value / 60)}時間前`;
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

.table-actions {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}

.create-label {
  text-decoration: none;
  font-weight: 700;
  color: #1f2937;
  cursor: pointer;
}

.create-label:hover {
  text-decoration: underline;
}

.tasks-table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;
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

.action-head {
  width: 72px;
  min-width: 72px;
  max-width: 72px;
  padding: 0;
  border: 0;
  background: transparent;
}

.action-cell {
  width: 72px;
  min-width: 72px;
  max-width: 72px;
  padding: 0 0 0 12px;
  border: 0;
  background: transparent;
  text-align: center;
}

.action-cell .delete-btn {
  width: 48px;
  height: 28px;
  border: 1px solid #4b5563;
  background: #fff;
  color: #111827;
  font: inherit;
  cursor: pointer;
}

.action-cell .delete-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.empty {
  text-align: center;
  color: #6b7280;
}
</style>
