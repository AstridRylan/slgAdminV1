import api from './index'

export default {
  getGenerals() {
    return api.get('/api/generals/listall')
  },
  getGeneral(cfgId) {
    return api.get(`/api/generals/get_general/${cfgId}`)
  },
  getGeneralByName(name) {
    return api.get(`/api/generals/get_general_by_name/${name}`)
  },
  createGeneral(data) {
    return api.post('/api/generals/add_general', data)
  },
  updateGeneral(data) {
    return api.put('/api/generals/update_general', data)
  },
  deleteGeneral(cfgId) {
    return api.delete('/api/generals/del_general', { data: { cfgId: cfgId } })
  },
  uploadPortrait(cfgId, formData) {
    return api.post(`/api/generals/upload_portrait/${cfgId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}