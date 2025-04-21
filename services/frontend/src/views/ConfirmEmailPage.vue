<template>
  <div class="confirmation-page">
    <h1>Проверьте вашу почту</h1>
    <p>Мы отправили письмо с подтверждением на {{ $route.query.email || 'ваш email' }}</p>
    <router-link to="/">Вернуться на страницу входа</router-link>
  </div>
</template>


<style scoped>
.confirmation-page {
  text-align: center;
  padding: 2rem;
}
</style>
