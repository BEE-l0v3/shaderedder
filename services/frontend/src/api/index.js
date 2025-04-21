import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api/v1',
  withCredentials: false,
  headers: {
    'Content-Type': 'application/json'
  }
})

export default {
  post: (url, data, config) => apiClient.post(url, data, config),
  register: (data) => apiClient.post('/register/new', data),
  // Методы для аутентификации
  login(email, password) {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)
    formData.append('grant_type', 'password')
    
    return apiClient.post('/login/access-token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
  },
  
  testToken(token) {
  return apiClient.post('/login/test-token', null, {
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  }).catch(error => {
    if (error.response?.status === 405) {
      // Если POST не разрешен, пробуем GET
      return apiClient.get('/login/test-token', {
        headers: { Authorization: `Bearer ${token}` }
      });
    }
    throw error;
  });
},

  confirmRegistration(token) {
    return apiClient.post('/register/confirm', {
      access_token: token,
      token_type: "bearer"
    })
  }
}
