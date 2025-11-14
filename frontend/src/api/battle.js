import api from './index'

export default {
  simulate(data) {
    return api.post('/api/battle/simulate', data)
  }
}

