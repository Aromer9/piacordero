import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export function useApi() {
  async function getProducts(params = {}) {
    const { data } = await api.get('/products', { params })
    return data
  }

  async function getProduct(id) {
    const { data } = await api.get(`/products/${id}`)
    return data
  }

  async function getSiteContent() {
    const { data } = await api.get('/site-content')
    return data
  }

  async function getSectionContent(section) {
    const { data } = await api.get(`/site-content/${section}`)
    return data
  }

  return {
    getProducts,
    getProduct,
    getSiteContent,
    getSectionContent,
  }
}
