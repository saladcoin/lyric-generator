<template>
  <div class="loading-spinner" v-if="visible">
    <div class="spinner">
      <div class="note note-1">♪</div>
      <div class="note note-2">♫</div>
      <div class="note note-3">♪</div>
    </div>
    <p class="loading-text">{{ text }}</p>
    <div class="loading-bar">
      <div class="loading-bar-inner"></div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  visible: Boolean,
  text: { type: String, default: 'AI 正在构思歌词...' },
})
</script>

<style scoped>
.loading-spinner {
  display: flex; flex-direction: column; align-items: center;
  padding: 48px 20px 40px;
  animation: fadeIn 0.4s ease;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

.spinner {
  position: relative;
  width: 80px; height: 80px;
  display: flex; align-items: center; justify-content: center;
}
.note {
  position: absolute;
  font-size: 28px;
  color: rgba(102,126,234,0.6);
  animation: bounce 1.8s ease-in-out infinite;
}
.note-1 { animation-delay: 0s; }
.note-2 { font-size: 34px; animation-delay: 0.3s; color: rgba(240,147,251,0.6); }
.note-3 { animation-delay: 0.6s; }
@keyframes bounce {
  0%, 100% { transform: translateY(0) scale(1); opacity: 0.4; }
  50% { transform: translateY(-16px) scale(1.1); opacity: 1; }
}

.loading-text {
  margin-top: 20px;
  color: rgba(255,255,255,0.5);
  font-size: 14px;
  letter-spacing: 1px;
}

.loading-bar {
  width: 160px; height: 3px;
  background: rgba(255,255,255,0.06);
  border-radius: 4px;
  margin-top: 16px;
  overflow: hidden;
}
.loading-bar-inner {
  width: 40%; height: 100%;
  background: linear-gradient(90deg, #667eea, #f093fb);
  border-radius: 4px;
  animation: barSlide 1.4s ease-in-out infinite;
}
@keyframes barSlide {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(350%); }
}
</style>
