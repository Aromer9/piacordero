import axios from 'axios'
import { getToken, clearToken } from './useAuth.js'

function adminClient() {
  const token = getToken()
  const client = axios.create({
    baseURL: '/api',
    timeout: 15000,
    headers: token ? { Authorization: `Bearer ${token}` } : {},
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
    const { data } = await adminClient().post('/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
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
