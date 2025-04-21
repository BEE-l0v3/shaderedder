<template>
  <form @submit.prevent="handleRegister">
    <h1>РЕГИСТРАЦИЯ</h1>
    
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
      <label for="email">Email</label>
      <input 
        id="email" 
        type="email" 
        v-model="email"
        placeholder="введите email"
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
    
    <button type="submit">Зарегистрироваться</button>
    
    <span class="toggle-link" @click="goToLogin">
      Есть аккаунт? Войти
    </span>
  </form>
</template>

<script>
import api from '@/api'

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      error: ''
    }
  },
  methods: {
    async handleRegister() {
  try {
    const response = await api.post('/register/new', {
      username: this.username,
      email: this.email,
      password: this.password
    });

    if (response.data.success) {
      // Сохраняем токен для активации
      localStorage.setItem('activation_token', response.data.activation_token);
      this.$router.push('/confirm-email');
    }
  } catch (error) {
    this.error = error.response?.data?.detail || 'Registration failed';
  }
},
    goToLogin() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
form {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
}
.error-message {
  color: red;
}
</style>
