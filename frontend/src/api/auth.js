import api from './index'

export default {
  login(data) {
    return api.post('/api/auth/login', data)
  },
  register(data) {
    return api.post('/api/auth/register', data)
  },
  me() {
    return api.get('/api/auth/me')
  }
}

