<template>
  <section class="panel" aria-label="task-create-view">
    <div class="form-wrap">
      <h1 class="panel-title">タスク新規作成</h1>

      <form class="task-form" aria-label="task-create-form" @submit.prevent>
        <label class="field">
          <span class="field-label">やること</span>
          <input type="text" class="input" />
        </label>

        <label class="field">
          <span class="field-label">やる人</span>
          <select v-model="assigneeId" class="input">
            <option value="">選択してください</option>
            <option
              v-for="family in families"
              :key="family.id"
              :value="String(family.id)"
            >
              {{ family.name }}
            </option>
          </select>
          <p v-if="familyError" class="field-error">{{ familyError }}</p>
        </label>

        <label class="field">
          <span class="field-label">期限</span>
          <VueDatePicker
            v-model="dueDate"
            :locale="ja"
            :enable-time-picker="true"
            :format="'yyyy/MM/dd HH:mm'"
            placeholder=""
            class="date-picker"
          />
        </label>

        <label class="field">
          <span class="field-label">進行状況</span>
          <select v-model="status" class="input">
            <option value="未対応">未対応</option>
            <option value="進行中">進行中</option>
            <option value="完了">完了</option>
          </select>
        </label>

        <label class="field">
          <span class="field-label">アラーム</span>
          <p class="field-help">何分前にアラームをかけますか</p>
          <select v-model="alarmMinutes" class="input">
            <option value="">選択してください</option>
            <option value="none">未設定</option>
            <option
              v-for="minutes in alarmMinuteOptions"
              :key="minutes"
              :value="String(minutes)"
            >
              {{ formatAlarmLead(minutes) }}
            </option>
          </select>
        </label>

        <div class="actions">
          <button type="button" class="action-btn">戻る</button>
          <button type="submit" class="action-btn">保存</button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup>
import { onMounted, ref } from "vue";
import { VueDatePicker } from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import { ja } from "date-fns/locale";

const assigneeId = ref("");
const status = ref("未対応");
const dueDate = ref(null);
const alarmMinutes = ref("");
const families = ref([]);
const familyError = ref("");
const alarmMinuteOptions = [5, 10, 15, 30, 60, 120, 180, 360, 720, 1440];

const formatAlarmLead = (value) => {
  if (value % 1440 === 0) return `${value / 1440}日前`;
  if (value % 60 === 0) return `${value / 60}時間前`;
  return `${value}分前`;
};

const loadFamilies = async () => {
  familyError.value = "";
  try {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || "";
    const response = await fetch(`${baseUrl}/auth/families/`);
    const data = await response.json();
    if (!response.ok) {
      familyError.value = data?.error || "家族一覧の取得に失敗しました。";
      families.value = [];
      return;
    }
    families.value = Array.isArray(data?.families) ? data.families : [];
  } catch {
    familyError.value = "家族一覧の取得に失敗しました。";
    families.value = [];
  }
};

onMounted(loadFamilies);
</script>

<style scoped>
.panel {
  --form-control-text: #1f2937;
  min-height: 100%;
  padding: 28px;
  box-sizing: border-box;
}

.form-wrap {
  width: min(460px, 100%);
}

.panel-title {
  margin: 0 0 18px;
  font-size: 1.25rem;
  letter-spacing: 0.04em;
}

.task-form {
  display: grid;
  gap: 12px;
}

.field {
  display: grid;
  gap: 6px;
}

.field-label {
  font-size: 0.82rem;
  color: #374151;
}

.field-error {
  margin: 0;
  color: #b91c1c;
  font-size: 0.78rem;
}

.field-help {
  margin: 0;
  color: #374151;
  font-size: 0.78rem;
}

.input {
  height: 30px;
  border: 1px solid #6b7280;
  padding: 0 8px;
  font: inherit;
  color: var(--form-control-text);
  background: #fff;
}

.date-picker {
  width: 100%;
}

:deep(.dp__input) {
  height: 30px;
  border: 1px solid #6b7280;
  border-radius: 0;
  padding: 0 8px;
  font: inherit;
  color: var(--form-control-text);
  box-shadow: none;
}

:deep(.dp__input::placeholder) {
  color: var(--form-control-text);
  opacity: 1;
}

:deep(.dp__input_icon) {
  pointer-events: none;
}

.actions {
  display: flex;
  gap: 12px;
  margin-top: 10px;
}

.action-btn {
  min-width: 84px;
  height: 34px;
  border: 1px solid #4b5563;
  background: #fff;
  font: inherit;
  cursor: pointer;
}
</style>
