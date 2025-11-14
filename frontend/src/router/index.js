import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'HomePage',
    component: () => import('../views/HomePage.vue')
  },
  {
    path: '/generals',
    name: 'GeneralList',
    component: () => import('../views/generals/GeneralList.vue')
  },
  {
    path: '/generals/add',
    name: 'AddGeneral',
    component: () => import('../views/generals/GeneralForm.vue')
  },
  {
    path: '/generals/edit/:id',
    name: 'EditGeneral',
    component: () => import('../views/generals/GeneralForm.vue')
  },
  {
    path: '/skills',
    name: 'SkillList',
    component: () => import('../views/skills/SkillList.vue')
  },
  {
    path: '/skills/add',
    name: 'AddSkill',
    component: () => import('../views/skills/SkillForm.vue')
  },
  {
    path: '/skills/edit/:id',
    name: 'EditSkill',
    component: () => import('../views/skills/SkillForm.vue')
  }
  ,
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/auth/Register.vue')
  },
  {
    path: '/battle',
    name: 'BattleSim',
    component: () => import('../views/battle/BattleSim.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
