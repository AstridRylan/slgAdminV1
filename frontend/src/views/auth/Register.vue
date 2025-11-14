<template>
  <div class="container">
    <div class="page-header">
      <h1>注册</h1>
    </div>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="100px" class="form-container">
      <el-form-item label="用户名" prop="username">
        <el-input v-model="form.username" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="密码" prop="password">
        <el-input v-model="form.password" type="password" placeholder="请输入密码" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submit">注册</el-button>
        <el-button @click="$router.push('/login')">去登录</el-button>
      </el-form-item>
    </el-form>
  </div>
  </template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import authApi from '@/api/auth'

const router = useRouter()
const formRef = ref(null)
const form = ref({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const submit = async () => {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    try {
      await authApi.register(form.value)
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } catch (e) {
      ElMessage.error(e?.response?.data?.error || '注册失败')
    }
  })
}
</script>

<style scoped>
</style>

