<template>
    <div class="activation-container">
      <h1 v-if="success">Аккаунт успешно активирован!</h1>
      <h1 v-else-if="error">{{ error }}</h1>
      <h1 v-else>Активация аккаунта...</h1>
  
      <router-link 
        v-if="success || error"
        to="/" 
        class="auth-link"
      >
        Перейти на страницу входа
      </router-link>
    </div>
  </template>
  
  <script>
  import api from '@/api'
  
  export default {
    data() {
      return {
        success: false,
        error: null
      }
    },
    async created() {
      const token = this.$route.query.token
      if (!token) {
        this.error = 'Отсутствует токен активации'
        return
      }
  
      try {
        const response = await api.post('/register/confirm', {
          access_token: token,
          token_type: 'bearer'
        })
  
        if (response.data.success) {
          this.success = true
        } else {
          this.error = response.data.comment || 'Ошибка активации'
        }
      } catch (err) {
        this.error = 'Серверная ошибка при активации'
        console.error(err)
      }
    },
    async mounted() {
  const token = localStorage.getItem('activation_token');
  if (!token) {
    this.error = 'No activation token found';
    return;
  }

  try {
    const response = await api.post('/register/confirm', {
      access_token: token,
      token_type: 'bearer'
    });

    if (response.data.success) {
      this.success = true;
      localStorage.removeItem('activation_token');
    }
  } catch (error) {
    this.error = error.response?.data?.detail || 'Activation failed';
  }
}
  }
  </script>
  
  <style scoped>
  .activation-container {
    max-width: 600px;
    margin: 2rem auto;
    padding: 2rem;
    text-align: center;
  }
  
  .auth-link {
    display: inline-block;
    margin-top: 1rem;
    color: #42b983;
  }
  </style>
