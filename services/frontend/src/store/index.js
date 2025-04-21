import { createStore } from 'vuex'
import api from '@/api'

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('authToken') || null
  },
  mutations: {
    setUser(state, user) {
      state.user = user
    },
    setToken(state, token) {
      state.token = token
      localStorage.setItem('authToken', token)
    },
    logout(state) {
      state.user = null
      state.token = null
      localStorage.removeItem('authToken')
    }
  },
  actions: {
    async login({ commit }, { email, password }) {
      const response = await api.login(email, password)
      commit('setToken', response.data.access_token)
      
      const userResponse = await api.testToken(response.data.access_token)
      commit('setUser', userResponse.data)
    },
    
    // Исправленный register action без неиспользуемых параметров
    async register(_, { username, email, password }) {
      await api.register(username, email, password)
    },
    
    async checkAuth({ commit, state }) {
      if (state.token) {
        try {
          const response = await api.testToken(state.token)
          commit('setUser', response.data)
          return true
        } catch {
          commit('logout')
          return false
        }
      }
      return false
    },
    
    logout({ commit }) {
      commit('logout')
    }
  },
  getters: {
    isAuthenticated: state => !!state.token,
    currentUser: state => state.user
  }
})