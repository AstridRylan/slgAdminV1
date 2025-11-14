<template>
  <div class="container">
    <div class="page-header">
      <h1>战法列表</h1>
      <el-button type="primary" @click="$router.push('/skills/add')">添加战法</el-button>
    </div>

    <el-table :data="skills" style="width: 100%" v-loading="loading">
      <el-table-column prop="cfgId" label="ID" width="80" />
      <el-table-column prop="name" label="名称" width="150" />
      <el-table-column label="适配兵种" width="200">
        <template #default="scope">
          <div class="troop-types">
            <el-tag v-if="scope.row.cavalry" size="small" type="success">骑兵</el-tag>
            <el-tag v-if="scope.row.archer" size="small" type="warning">弓兵</el-tag>
            <el-tag v-if="scope.row.shield" size="small" type="info">盾兵</el-tag>
            <el-tag v-if="scope.row.spear" size="small" type="danger">枪兵</el-tag>
            <el-tag v-if="scope.row.siege" size="small" type="primary">器械</el-tag>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="description" label="战法描述" />
      <el-table-column label="操作" width="150">
        <template #default="scope">
          <el-button size="small" @click="$router.push(`/skills/edit/${scope.row.cfgId}`)">编辑</el-button>
          <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import skillApi from '@/api/skill'

const skills = ref([])
const loading = ref(false)

// 模拟数据
const mockSkills = [
  {
    cfgId: 1, 
    name: '火攻奇谋',
    cavalry: false,
    archer: true,
    shield: false,
    spear: false,
    siege: true,
    description: '对敌军施放火攻，造成范围伤害并有几率造成灼烧效果'
  },
  {
    cfgId: 2, 
    name: '铁骑冲阵',
    cavalry: true,
    archer: false,
    shield: false,
    spear: true,
    siege: false,
    description: '率领部队冲锋，对直线敌军造成伤害并有几率击退'
  }
]

const fetchSkills = async () => {
  loading.value = true
  try {
    const res = await skillApi.getSkills()
    skills.value = res
  } catch (error) {
    console.error('获取战法列表失败:', error)
    ElMessage.error('获取战法列表失败')
  } finally {
    loading.value = false
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除战法 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await skillApi.deleteSkill(row.cfgId)
      skills.value = skills.value.filter(item => item.cfgId !== row.cfgId)
      ElMessage.success('删除成功')
    } catch (error) {
      console.error('删除战法失败:', error)
      ElMessage.error('删除战法失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchSkills()
})
</script>