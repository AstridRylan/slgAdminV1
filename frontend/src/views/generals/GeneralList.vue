<template>
  <div class="container">
    <div class="page-header">
      <h1>武将列表</h1>
      <el-button type="primary" @click="$router.push('/generals/add')">添加武将</el-button>
    </div>

    <div class="table-scroll">
      <el-table :data="generals" style="min-width: 1200px" v-loading="loading" border>
        <el-table-column prop="cfgId" label="ID" width="80" fixed="left" />
        <el-table-column label="立绘" width="100" fixed="left">
          <template #default="scope">
            <el-image
              v-if="scope.row.portrait"
              :src="scope.row.portrait"
              fit="cover"
              class="portrait-thumb"
              :preview-src-list="[scope.row.portrait]"
            />
            <div v-else class="portrait-thumb placeholder">暂无</div>
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" width="120" fixed="left" />
        <el-table-column prop="faction" label="阵营" width="120" />
        <el-table-column label="星级" width="160">
          <template #default="scope">
            <el-rate v-model="scope.row.stars" disabled class="yin-yang-rate" :max="5" />
          </template>
        </el-table-column>
        <el-table-column label="自带战法" width="120" show-overflow-tooltip>
          <template #default="scope">
            <el-tag type="warning" v-if="scope.row.innateSkillId">
              {{ skillNameById(scope.row.innateSkillId) }}
            </el-tag>
            <span v-else class="text-muted">未设置</span>
          </template>
        </el-table-column>
        <el-table-column label="六维属性" width="380">
          <template #default="scope">
            <div class="attributes">
              <div class="row">
                <span>武力: {{ scope.row.power }}<span class="growth">(+{{ formatGrowth(scope.row.powerGrowth) }})</span></span>
                <span>智力: {{ scope.row.intelligence }}<span class="growth">(+{{ formatGrowth(scope.row.intelligenceGrowth) }})</span></span>
                <span>统率: {{ scope.row.command }}<span class="growth">(+{{ formatGrowth(scope.row.commandGrowth) }})</span></span>
              </div>
              <div class="row">
                <span>速度: {{ scope.row.speed }}<span class="growth">(+{{ formatGrowth(scope.row.speedGrowth) }})</span></span>
                <span>政治: {{ scope.row.politics }}<span class="growth">(+{{ formatGrowth(scope.row.politicsGrowth) }})</span></span>
                <span>魅力: {{ scope.row.charm }}<span class="growth">(+{{ formatGrowth(scope.row.charmGrowth) }})</span></span>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="兵种适性" width="300">
          <template #default="scope">
            <div class="troop-types">
              <span>骑: {{ scope.row.cavalry }}</span>
              <span>弓: {{ scope.row.archer }}</span>
              <span>盾: {{ scope.row.shield }}</span>
              <span>枪: {{ scope.row.spear }}</span>
              <span>器械: {{ scope.row.siege }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="赛季限定" width="120">
          <template #default="scope">
            <el-tag :type="scope.row.seasonLimit === '全赛季' ? 'success' : 'warning'">
              {{ scope.row.seasonLimit }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="是否SP" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.isSP === '是' ? 'danger' : 'info'">
              {{ scope.row.isSP }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right" align="center">
          <template #default="scope">
            <div class="op-column">
              <el-button size="small" @click="$router.push(`/generals/edit/${scope.row.cfgId}`)">编辑</el-button>
              <el-button size="small" type="danger" @click="handleDelete(scope.row)">删除</el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessageBox, ElMessage } from 'element-plus'
import generalApi from '@/api/general'
import skillApi from '@/api/skill'

const generals = ref([])
const loading = ref(false)

// 后端战法列表缓存（页面加载时一次性获取）
const skills = ref([])
const fetchSkills = async () => {
  try {
    const res = await skillApi.getSkills()
    skills.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('获取战法列表失败:', error)
    ElMessage.error('获取战法列表失败')
  }
}

const mockGenerals = [
  {
    cfgId: 1,
    name: '关羽',
    faction: '蜀',
    stars: 5,
    seasonLimit: '全赛季',
    isSP: '否',
    power: 98,
    powerGrowth: 0.9,
    command: 95,
    commandGrowth: 0.8,
    intelligence: 80,
    intelligenceGrowth: 0.6,
    speed: 75,
    speedGrowth: 0.5,
    politics: 70,
    politicsGrowth: 0.4,
    charm: 90,
    charmGrowth: 0.7,
    cavalry: 'S',
    archer: 'C',
    shield: 'B',
    spear: 'A',
    siege: 'C',
    portrait: 'https://via.placeholder.com/64x64.png?text=%E5%85%AC%E5%90%9B',
    innateSkillId: 101,
    biography: '字云长，河东解良人...'
  },
  {
    cfgId: 2,
    name: '诸葛亮',
    faction: '蜀',
    stars: 5,
    seasonLimit: 'S2赛季',
    isSP: '是',
    power: 65,
    powerGrowth: 0.4,
    command: 95,
    commandGrowth: 0.8,
    intelligence: 100,
    intelligenceGrowth: 1.0,
    speed: 70,
    speedGrowth: 0.5,
    politics: 95,
    politicsGrowth: 0.9,
    charm: 90,
    charmGrowth: 0.7,
    cavalry: 'C',
    archer: 'A',
    shield: 'B',
    spear: 'B',
    siege: 'S',
    portrait: 'https://via.placeholder.com/64x64.png?text=%E4%B8%BB%E5%B0%8A',
    innateSkillId: 103,
    biography: '字孔明，号卧龙...'
  }
]

const fetchGenerals = async () => {
  loading.value = true
  try {
    const res = await generalApi.getGenerals()
    generals.value = res
    console.log('获取武将列表成功:', res)
  } catch (error) {
    console.error('获取武将列表失败:', error)
    ElMessage.error('获取武将列表失败')
  } finally {
    loading.value = false
  }
}

const skillNameById = (cfgId) => {
  const s = skills.value.find((x) => x.cfgId === cfgId)
  return s ? s.name : '未知战法'
}

const formatGrowth = (v) => Number(v || 0).toFixed(2)

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定要删除武将 ${row.name} 吗？`, '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await generalApi.deleteGeneral(row.cfgId)
      generals.value = generals.value.filter(item => item.cfgId !== row.cfgId)
      ElMessage.success('删除成功')
    } catch (error) {
      console.error('删除武将失败:', error)
      ElMessage.error('删除武将失败')
    }
  }).catch(() => {})
}

onMounted(() => {
  fetchGenerals()
  fetchSkills()
})
</script>

<style scoped>
.table-scroll {
  width: 100%;
  overflow-x: auto;
}
.portrait-thumb {
  width: 64px;
  height: 96px; /* 2:3 比例 */
  border-radius: 6px;
  overflow: hidden;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #909399;
}
.portrait-thumb.placeholder {
  border: 1px dashed #dcdfe6;
}

.op-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  height: 100%;
}
.op-column .el-button {
  width: 88px;
  margin: 0 auto;
}

.yin-yang-rate .el-rate__icon {
  position: relative;
  color: transparent;
  width: 1.4em;
  height: 1.4em;
}
.yin-yang-rate .el-rate__icon::before {
  content: '';
  display: block;
  width: 100%;
  height: 100%;
  background-repeat: no-repeat;
  background-size: contain;
  background-position: center;
  /* 金色半阴阳鱼 SVG */
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cg fill='%23FFD700'%3E%3Cpath d='M50 5a45 45 0 1 0 0 90c-12.5 0-22.5-10.1-22.5-22.5S37.5 50 50 50s22.5-10.1 22.5-22.5S62.5 5 50 5z'/%3E%3Ccircle cx='62.5' cy='27.5' r='7.5' fill='%23fff2b3'/%3E%3Ccircle cx='37.5' cy='72.5' r='7.5' fill='%23ccad00'/%3E%3C/g%3E%3C/svg%3E");
  filter: drop-shadow(0 1px 0 rgba(0,0,0,0.1));
}

.text-muted {
  color: #909399;
}

.attributes .row {
  display: flex;
  gap: 16px;
  margin-bottom: 4px;
}
.attributes .row span {
  white-space: nowrap;
}
.attributes .growth {
  color: #67C23A; /* Element Plus success green */
  margin-left: 2px;
}
</style>