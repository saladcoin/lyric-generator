import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

export async function generateLyrics(files, style, emotion, theme, extra) {
  const form = new FormData()
  for (const f of files) {
    form.append('files', f)
  }
  form.append('style', style)
  form.append('emotion', emotion)
  if (theme) form.append('theme', theme)
  if (extra) form.append('extra', extra)

  const res = await api.post('/generate', form)
  return res.data
}

export async function healthCheck() {
  const res = await api.get('/health')
  return res.data
}
