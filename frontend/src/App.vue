<template>
  <el-container class="layout-container">
    <el-aside width="200px">
      <el-menu
        router
        default-active="/"
        class="el-menu-vertical"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">
        <el-menu-item index="/">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-sub-menu index="/generals">
          <template #title>
            <el-icon><User /></el-icon>
            <span>武将管理</span>
          </template>
          <el-menu-item index="/generals">武将列表</el-menu-item>
          <el-menu-item index="/generals/add">添加武将</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="/skills">
          <template #title>
            <el-icon><MagicStick /></el-icon>
            <span>战法管理</span>
          </template>
          <el-menu-item index="/skills">战法列表</el-menu-item>
          <el-menu-item index="/skills/add">添加战法</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="/battle">
          <el-icon><MagicStick /></el-icon>
          <span>模拟战斗</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <h2>SLG后台管理系统</h2>
        <div style="margin-left:auto;display:flex;align-items:center;gap:12px;">
          <el-avatar :src="avatarUrl || defaultAvatar" size="small" />
          <span>{{ username || '未登录' }}</span>
          <el-button v-if="!username" size="small" @click="$router.push('/login')">去登录</el-button>
          <el-dropdown v-else>
            <span class="el-dropdown-link">
              操作<el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
      <el-footer>© v1.0 SLG后台管理系统</el-footer>
    </el-container>
  </el-container>
</template>

<script setup>
import { House, User, MagicStick, ArrowDown } from '@element-plus/icons-vue'
import { ref, onMounted } from 'vue'
import authApi from '@/api/auth'

const username = ref(localStorage.getItem('username') || '')
const avatarUrl = ref(localStorage.getItem('avatarUrl') || '')
const defaultAvatar = '/resources/skin/skill/default_bingren.png'

const refreshMe = async () => {
  try {
    const me = await authApi.me()
    username.value = me.username
    avatarUrl.value = me.avatarUrl || ''
  } catch {}
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('username')
  localStorage.removeItem('avatarUrl')
  username.value = ''
  avatarUrl.value = ''
}

onMounted(() => {
  if (localStorage.getItem('token')) refreshMe()
})
</script>

<style>
.layout-container {
  height: 100vh;
}

.el-header {
  background-color: #545c64;
  color: #fff;
  line-height: 60px;
  display: flex;
  align-items: center;
  padding: 0 16px;
  box-shadow: 0 1px 0 rgba(0, 0, 0, 0.08);
}

.el-header h2 {
  margin: 0;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.el-aside {
  background-color: #545c64;
  color: #fff;
}

.el-menu-vertical {
  height: 100%;
  border-right: none;
}

.el-footer {
  background-color: #f5f7fa;
  color: #333;
  text-align: center;
  line-height: 60px;
  border-top: 1px solid #dcdfe6;
}
</style>
