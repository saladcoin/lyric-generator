<template>
  <div class="style-config">
    <div class="config-section">
      <label class="config-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M9 18V5l12-2v13" stroke-linecap="round" stroke-linejoin="round"/>
          <circle cx="6" cy="18" r="3"/><circle cx="18" cy="16" r="3"/>
        </svg>
        曲风
      </label>
      <div class="btn-group">
        <button v-for="s in styles" :key="s.value"
          :class="['btn-option', { active: selectedStyle === s.value }]"
          @click="selectedStyle = s.value">
          <span class="option-icon">{{ s.icon }}</span>
          {{ s.label }}
        </button>
      </div>
    </div>

    <div class="config-section">
      <label class="config-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M20.84 4.61a5.5 5.5 0 00-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 00-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 000-7.78z" stroke-linecap="round"/>
        </svg>
        情感基调
      </label>
      <div class="btn-group">
        <button v-for="e in emotions" :key="e.value"
          :class="['btn-option', 'btn-emotion', { active: selectedEmotion === e.value }]"
          @click="selectedEmotion = e.value">
          {{ e.label }}
        </button>
      </div>
    </div>

    <div class="config-row">
      <div class="config-section flex-1">
        <label class="config-label">📝 主题</label>
        <input class="config-input" v-model="theme" placeholder="例如：青春、梦想、离别..." />
      </div>
      <div class="config-section flex-1">
        <label class="config-label">✏️ 额外要求</label>
        <input class="config-input" v-model="extra" placeholder="例如：加入说唱部分..." />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const emit = defineEmits(['update'])

const styles = [
  { label: '流行', value: 'pop', icon: '🎤' },
  { label: '摇滚', value: 'rock', icon: '🎸' },
  { label: '古风', value: 'gufeng', icon: '🏮' },
  { label: 'R&B', value: 'rnb', icon: '🎹' },
  { label: '民谣', value: 'folk', icon: '🌿' },
  { label: '说唱', value: 'hiphop', icon: '🎧' },
]
const emotions = [
  { label: '欢快', value: '欢快' },
  { label: '伤感', value: '伤感' },
  { label: '激昂', value: '激昂' },
  { label: '温柔', value: '温柔' },
  { label: '浪漫', value: '浪漫' },
  { label: '深情', value: '深情' },
]

const selectedStyle = ref('pop')
const selectedEmotion = ref('欢快')
const theme = ref('')
const extra = ref('')

watch([selectedStyle, selectedEmotion, theme, extra], () => {
  emit('update', {
    style: selectedStyle.value,
    emotion: selectedEmotion.value,
    theme: theme.value,
    extra: extra.value,
  })
}, { immediate: true })
</script>

<style scoped>
.style-config { }
.config-section { margin-bottom: 18px; }
.config-label {
  display: flex; align-items: center; gap: 6px;
  font-size: 14px; font-weight: 600; color: rgba(255,255,255,0.7);
  margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.5px;
}
.config-label svg { opacity: 0.6; }

.btn-group { display: flex; flex-wrap: wrap; gap: 8px; }
.btn-option {
  display: flex; align-items: center; gap: 4px;
  padding: 8px 16px;
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  background: rgba(255,255,255,0.04);
  cursor: pointer;
  font-size: 14px;
  color: rgba(255,255,255,0.6);
  transition: all 0.25s ease;
}
.btn-option:hover {
  border-color: rgba(102,126,234,0.4);
  background: rgba(102,126,234,0.08);
  color: #e0e0e0;
}
.btn-option.active {
  background: linear-gradient(135deg, rgba(102,126,234,0.2), rgba(118,75,162,0.2));
  border-color: #667eea;
  color: #fff;
  box-shadow: 0 0 16px rgba(102,126,234,0.15);
}
.option-icon { font-size: 16px; }

.btn-emotion.active {
  background: linear-gradient(135deg, rgba(240,147,251,0.2), rgba(245,87,108,0.2));
  border-color: #f093fb;
  box-shadow: 0 0 16px rgba(240,147,251,0.15);
}

.config-row { display: flex; gap: 14px; }
.flex-1 { flex: 1; }
.config-input {
  width: 100%; padding: 10px 14px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 10px;
  font-size: 14px; color: #e0e0e0;
  outline: none; transition: all 0.25s;
  box-sizing: border-box;
}
.config-input::placeholder { color: rgba(255,255,255,0.25); }
.config-input:focus { border-color: #667eea; background: rgba(102,126,234,0.06); }

@media (max-width: 500px) {
  .config-row { flex-direction: column; gap: 0; }
}
</style>
