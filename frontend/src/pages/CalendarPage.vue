<template>
  <section class="panel" aria-label="calendar-view">
    <h1 class="panel-title">カレンダー</h1>
    <p class="panel-copy">タスクの予定をカレンダーで確認できます。</p>
  </section>
</template>

<style scoped>
.panel {
  min-height: 100%;
  border: 1px solid #c9d3e4;
  background: rgba(255, 255, 255, 0.88);
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
</style>
