import axios from 'axios'
import { getToken, clearToken } from './useAuth.js'
import { API_BASE } from '../config/api.js'

function adminClient() {
  const client = axios.create({
    baseURL: API_BASE,
    timeout: 15000,
  })

  client.interceptors.request.use((config) => {
    const token = getToken()
    if (token) {
      config.headers = config.headers ?? {}
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  })

  client.interceptors.response.use(
    (r) => r,
    (err) => {
      if (err.response?.status === 401) clearToken()
      return Promise.reject(err)
    }
  )
  return client
}

export function useAdminApi() {
  // Productos
  async function getProducts() {
    const { data } = await adminClient().get('/products')
    return data
  }

  async function createProduct(payload) {
    const { data } = await adminClient().post('/products', payload)
    return data
  }

  async function updateProduct(id, payload) {
    const { data } = await adminClient().put(`/products/${id}`, payload)
    return data
  }

  async function deleteProduct(id) {
    await adminClient().delete(`/products/${id}`)
  }

  async function updateProductOrder(id, order) {
    await adminClient().patch(`/products/${id}/order`, { order })
  }

  // Contenido del sitio
  async function getSiteContent() {
    const { data } = await adminClient().get('/site-content')
    return data
  }

  async function updateSiteContent(section, content) {
    const { data } = await adminClient().put(`/site-content/${section}`, { content })
    return data
  }

  // Upload de imagen
  async function uploadImage(file) {
    const form = new FormData()
    form.append('file', file)
    // No fijar Content-Type: axios añade multipart + boundary y no pisa Authorization.
    const { data } = await adminClient().post('/upload', form)
    return data
  }

  return {
    getProducts,
    createProduct,
    updateProduct,
    deleteProduct,
    updateProductOrder,
    getSiteContent,
    updateSiteContent,
    uploadImage,
  }
}
