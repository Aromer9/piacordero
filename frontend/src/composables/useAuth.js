import axios from 'axios'
import { ref } from 'vue'

const TOKEN_KEY = 'pia_admin_token'

export const isAuthenticated = ref(!!localStorage.getItem(TOKEN_KEY))

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token)
  isAuthenticated.value = true
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY)
  isAuthenticated.value = false
}

export function useAuth() {
  async function login(password) {
    const { data } = await axios.post('/api/auth/login', { password })
    setToken(data.access_token)
    return data
  }

  function logout() {
    clearToken()
  }

  return { login, logout, isAuthenticated, getToken }
}
