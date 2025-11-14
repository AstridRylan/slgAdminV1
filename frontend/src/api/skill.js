import api from './index'

export default {
  getSkills() {
    return api.get('/api/skills/listall')
  },
  getSkill(id) {
    return api.get(`/api/skills/get_skill/${id}`)
  },
  getSkillByName(name) {
    return api.get(`/api/skills/get_skill_by_name/${name}`)
  },
  createSkill(data) {
    return api.post('/api/skills/add_skill', data)
  },
  updateSkill(data) {
    return api.put(`/api/skills/update_skill`, data)
  },
  deleteSkill(cfgId) {
    return api.delete(`/api/skills/del_skill`, { data: { cfgId: cfgId } })
  },
  uploadPortrait(cfgId, formData) {
    return api.post(`/api/skills/upload_portrait/${cfgId}`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}