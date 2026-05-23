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
          <input type="text" class="input" />
        </label>

        <label class="field">
          <span class="field-label">進行状況</span>
          <input type="text" class="input" />
        </label>

        <label class="field">
          <span class="field-label">アラーム</span>
          <input type="text" class="input" />
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

const assigneeId = ref("");
const families = ref([]);
const familyError = ref("");

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

.input {
  height: 30px;
  border: 1px solid #6b7280;
  padding: 0 8px;
  font: inherit;
  background: #fff;
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
