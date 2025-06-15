import { createStore } from 'vuex'
import axios from 'axios'

const API_URL = 'http://localhost:8000/api'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || null,
    products: [],
    ingredients: [],
    orders: [],
    cart: []
  },
  
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    clearAuth(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('token')
    },
    setProducts(state, products) {
      state.products = products
    },
    setIngredients(state, ingredients) {
      state.ingredients = ingredients
    },
    setOrders(state, orders) {
      state.orders = orders
    },
    addToCart(state, item) {
      state.cart.push(item)
    },
    removeFromCart(state, index) {
      state.cart.splice(index, 1)
    },
    clearCart(state) {
      state.cart = []
    }
  },
  
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post(`${API_URL}/token/`, credentials)
        commit('setToken', response.data.access)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async register({ commit }, userData) {
      try {
        const response = await axios.post(`${API_URL}/users/`, userData)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async fetchProducts({ commit }) {
      try {
        const response = await axios.get(`${API_URL}/products/`)
        commit('setProducts', response.data)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async fetchIngredients({ commit }) {
      try {
        const response = await axios.get(`${API_URL}/ingredients/`)
        commit('setIngredients', response.data)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async createOrder({ commit, state }, orderData) {
      try {
        const response = await axios.post(`${API_URL}/orders/`, {
          order_items: state.cart.map(item => ({
            product_id: item.product.id,
            quantity: item.quantity,
            ingredients: item.selectedIngredients.map(ing => ({
              ingredient_id: ing.id,
              quantity: ing.quantity
            }))
          }))
        }, {
          headers: { Authorization: `Bearer ${state.token}` }
        })
        commit('clearCart')
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async fetchOrders({ commit, state }) {
      try {
        const response = await axios.get(`${API_URL}/orders/`, {
          headers: { Authorization: `Bearer ${state.token}` }
        })
        commit('setOrders', response.data)
        return response.data
      } catch (error) {
        throw error
      }
    },
    
    async updateOrderStatus({ state }, { orderId, status }) {
      try {
        const response = await axios.post(
          `${API_URL}/orders/${orderId}/${status}/`,
          {},
          { headers: { Authorization: `Bearer ${state.token}` } }
        )
        return response.data
      } catch (error) {
        throw error
      }
    }
  },
  
  getters: {
    isAuthenticated: state => !!state.token,
    isAdmin: state => state.user?.role === 'admin',
    cartTotal: state => {
      return state.cart.reduce((total, item) => {
        const basePrice = item.product.base_price * item.quantity
        const ingredientsPrice = item.selectedIngredients.reduce(
          (sum, ing) => sum + (ing.price * ing.quantity),
          0
        )
        return total + basePrice + ingredientsPrice
      }, 0)
    }
  }
}) 