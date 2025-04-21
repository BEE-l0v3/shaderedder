import api from '@/api'
import { createRouter, createWebHistory } from 'vue-router'
import LoginPage from '../views/LoginPage.vue'
import RegisterPage from '../views/RegisterPage.vue'
import WelcomePage from '../views/WelcomePage.vue'

const routes = [
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/welcome',
    name: 'WelcomePage',
    component: WelcomePage,
    meta: { requiresAuth: true }
  },
  {
    path: '/confirm-email',
    name: 'ConfirmEmailPage',
    component: () => import('@/views/ConfirmEmailPage.vue')
  },
  {
  path: '/activate-account',
  name: 'ActivateAccountPage',
  component: () => import('../views/ActivateAccountPage.vue'),
  props: route => ({ token: route.query.token })
},
  {
    path: '/',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('authToken');
  
  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login');
    } else {
      try {
        // Используем POST как в curl-запросе
        await api.post('/login/test-token', null, {
          headers: { Authorization: `Bearer ${token}` }
        });
        next();
      } catch (error) {
        console.error('Ошибка проверки токена:', error);
        localStorage.removeItem('authToken');
        next('/login');
      }
    }
  } else if (token && (to.name === 'LoginPage' || to.name === 'RegisterPage')) {
    next('/welcome');
  } else {
    next();
  }
});

export default router
