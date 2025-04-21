<template>
  <div v-if="!loading">
    <h1>Добро пожаловать, {{ user.username || 'Пользователь' }}!</h1>
    <p v-if="user.email">Email: {{ user.email }}</p>
    <p v-if="user.role">Роль: {{ roleNames[user.role] || user.role }}</p>
    
    <div v-if="!user.is_activated" class="activation-warning">
      Ваш аккаунт не активирован. Проверьте почту для подтверждения.
    </div>
    
    <button @click="handleLogout">Выйти</button>
  </div>
  <div v-else class="loading-indicator">
    Загрузка данных...
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'WelcomePage',
  data() {
    return {
      loading: true,
      user: {
        username: '',
        email: '',
        id: null,
        is_activated: false,
        role: null
      },
      roleNames: {
        1: 'Пользователь',
        2: 'Модератор',
        3: 'Администратор'
      }
    }
  },
  async created() {
    await this.fetchUserData()
  },
  methods: {
    async fetchUserData() {
      this.loading = true
      const token = localStorage.getItem('authToken')
      
      if (!token) {
        this.$router.push('/login')
        return
      }

      try {
        const response = await api.testToken(token)
        console.log('Данные пользователя:', response.data)  // Для отладки
        
        this.user = {
          username: response.data.username,
          email: response.data.email,
          id: response.data.id,
          is_activated: response.data.is_activated,
          role: response.data.role
        }
      } catch (error) {
        console.error('Ошибка:', {
          status: error.response?.status,
          data: error.response?.data,
          config: error.config
        })
        this.handleLogout()
      } finally {
        this.loading = false
      }
    },
    handleLogout() {
      localStorage.removeItem('authToken')
      this.$router.push('/login')
    }
  }
}
</script>

<style scoped>
.activation-warning {
  color: #ff9800;
  margin: 20px 0;
  padding: 10px;
  background: #fff3e0;
  border-radius: 4px;
}

button {
  margin-top: 20px;
  padding: 10px 20px;
  background: #ff4444;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.loading-indicator {
  padding: 20px;
  text-align: center;
  color: #666;
}
</style>
