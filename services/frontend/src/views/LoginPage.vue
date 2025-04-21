<template>
  <form @submit.prevent="handleLogin">
    <h1>ВХОД</h1>
    
    <div v-if="error" class="error-message">
      {{ error }}
    </div>
    
    <div>
      <label for="username">Имя пользователя</label>
      <input 
        id="username" 
        type="text" 
        v-model="username" 
        placeholder="введите username" 
        required
      >
    </div>
    
    <div>
      <label for="password">Пароль</label>
      <input 
        id="password" 
        type="password" 
        v-model="password" 
        placeholder="введите password" 
        required
      >
    </div>
    
    <button type="submit" :disabled="loading">
      {{ loading ? 'Загрузка...' : 'Войти' }}
    </button>
    
    <span class="toggle-link" @click="goToRegister">
      Нет аккаунта? Зарегистрироваться
    </span>
  </form>
</template>

<script>
import api from '@/api'

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      error: '',
      loading: false
    }
  },
  methods: {
    async handleLogin() {
  this.loading = true;
  this.error = '';
  
  try {
    const formData = new URLSearchParams();
    formData.append('username', this.username);
    formData.append('password', this.password);
    formData.append('grant_type', 'password');

    const response = await api.post('/login/access-token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    const token = response.data.access_token;
    if (!token) throw new Error('Токен не получен');
    
    localStorage.setItem('authToken', token);
    
    // Явный редирект с полным путем
    window.location.href = '/welcome'; // Используем полный редирект
    
  } catch (error) {
    console.error('Ошибка входа:', error);
    if (error.response?.status === 400 || error.response?.status === 401) {
      this.error = 'Неверный логин или пароль';
    } else {
      this.error = error.message || 'Ошибка соединения с сервером';
    }
  } finally {
    this.loading = false;
  }
},
    goToRegister() {
      this.$router.push('/register');
    }
  }
}
</script>

<style scoped>
.error-message {
  color: #ff4444;
  margin-bottom: 15px;
}
</style>
