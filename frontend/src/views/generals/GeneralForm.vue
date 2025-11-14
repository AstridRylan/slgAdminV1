<template>
  <div class="container">
    <div class="page-header">
      <h1>{{ isEdit ? '编辑武将' : '添加武将' }}</h1>
    </div>

    <el-form 
      ref="formRef" 
      :model="form" 
      :rules="rules" 
      label-width="120px" 
      class="form-container"
      v-loading="loading">
      
      <el-form-item label="武将名称" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>
      
      <el-form-item label="阵营" prop="faction">
        <el-select v-model="form.faction" placeholder="请选择阵营">
          <el-option label="魏" value="魏" />
          <el-option label="蜀" value="蜀" />
          <el-option label="吴" value="吴" />
          <el-option label="群" value="群" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="赛季限定" prop="seasonLimit">
        <el-select v-model="form.seasonLimit" placeholder="请选择赛季">
          <el-option label="全赛季" value="全赛季" />
          <el-option label="S2赛季" value="S2赛季" />
          <el-option label="S3赛季" value="S3赛季" />
          <el-option label="PK赛季" value="PK赛季" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="是否SP" prop="isSP">
        <el-radio-group v-model="form.isSP">
          <el-radio label="是">是</el-radio>
          <el-radio label="否">否</el-radio>
        </el-radio-group>
      </el-form-item>
      
      <el-form-item label="星级" prop="stars">
        <el-rate v-model="form.stars" :max="5" class="yin-yang-rate" />
      </el-form-item>
      
      <el-divider content-position="left">六维属性</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="武力" prop="power">
            <el-input-number v-model="form.power" :min="1" :max="100" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="统率" prop="command">
            <el-input-number v-model="form.command" :min="1" :max="100" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="智力" prop="intelligence">
            <el-input-number v-model="form.intelligence" :min="1" :max="100" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="速度" prop="speed">
            <el-input-number v-model="form.speed" :min="1" :max="100" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="政治" prop="politics">
            <el-input-number v-model="form.politics" :min="1" :max="100" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="魅力" prop="charm">
            <el-input-number v-model="form.charm" :min="1" :max="100" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-divider content-position="left">成长值</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="武力成长" prop="powerGrowth">
            <el-input-number v-model="form.powerGrowth" :min="0" :max="10" :step="0.1" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="统率成长" prop="commandGrowth">
            <el-input-number v-model="form.commandGrowth" :min="0" :max="10" :step="0.1" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="智力成长" prop="intelligenceGrowth">
            <el-input-number v-model="form.intelligenceGrowth" :min="0" :max="10" :step="0.1" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="速度成长" prop="speedGrowth">
            <el-input-number v-model="form.speedGrowth" :min="0" :max="10" :step="0.1" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="政治成长" prop="politicsGrowth">
            <el-input-number v-model="form.politicsGrowth" :min="0" :max="10" :step="0.1" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="魅力成长" prop="charmGrowth">
            <el-input-number v-model="form.charmGrowth" :min="0" :max="10" :step="0.1" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-divider content-position="left">兵种适性</el-divider>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="骑兵适性" prop="cavalry">
            <el-select v-model="form.cavalry" placeholder="请选择">
              <el-option label="S" value="S" />
              <el-option label="A" value="A" />
              <el-option label="B" value="B" />
              <el-option label="C" value="C" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="弓兵适性" prop="archer">
            <el-select v-model="form.archer" placeholder="请选择">
              <el-option label="S" value="S" />
              <el-option label="A" value="A" />
              <el-option label="B" value="B" />
              <el-option label="C" value="C" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="盾兵适性" prop="shield">
            <el-select v-model="form.shield" placeholder="请选择">
              <el-option label="S" value="S" />
              <el-option label="A" value="A" />
              <el-option label="B" value="B" />
              <el-option label="C" value="C" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="枪兵适性" prop="spear">
            <el-select v-model="form.spear" placeholder="请选择">
              <el-option label="S" value="S" />
              <el-option label="A" value="A" />
              <el-option label="B" value="B" />
              <el-option label="C" value="C" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="器械适性" prop="siege">
            <el-select v-model="form.siege" placeholder="请选择">
              <el-option label="S" value="S" />
              <el-option label="A" value="A" />
              <el-option label="B" value="B" />
              <el-option label="C" value="C" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="立绘上传" prop="portrait">
        <el-upload
          class="avatar-uploader"
          action="#"
          :show-file-list="false"
          :before-upload="beforeAvatarUpload"
          :http-request="handleUpload">
          <img v-if="form.portrait" :src="form.portrait" class="avatar" />
          <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
        </el-upload>
      </el-form-item>
      
      <el-form-item label="自带战法" prop="innateSkillId">
        <div class="innate-skill-field">
          <el-tag type="warning" v-if="form.innateSkillId">{{ skillNameById(form.innateSkillId) }}</el-tag>
          <span v-else class="text-muted">未选择</span>
          <el-button size="small" @click="openSkillDialog('innate')" class="ml8">选择战法</el-button>
          <el-button size="small" type="danger" @click="form.innateSkillId = null" class="ml8">清除</el-button>
        </div>
      </el-form-item>

      <el-form-item label="传承战法" prop="heritageSkillId">
        <div class="innate-skill-field">
          <el-tag type="info" v-if="form.heritageSkillId">{{ skillNameById(form.heritageSkillId) }}</el-tag>
          <span v-else class="text-muted">未选择</span>
          <el-button size="small" @click="openSkillDialog('heritage')" class="ml8">选择战法</el-button>
          <el-button size="small" type="danger" @click="form.heritageSkillId = null" class="ml8">清除</el-button>
        </div>
      </el-form-item>

      <el-dialog v-model="skillDialogVisible" title="选择战法" width="520px" :close-on-click-modal="false">
        <el-input v-model="skillSearch" placeholder="搜索技能ID或名称" clearable />
        <el-table :data="filteredSkills" height="320" @row-click="onSelectSkill" class="mt12">
          <el-table-column prop="cfgId" label="ID" width="100" />
          <el-table-column prop="name" label="名称" />
        </el-table>
        <template #footer>
          <el-button @click="skillDialogVisible = false">关闭</el-button>
        </template>
      </el-dialog>
      
      <el-form-item label="个人生平" prop="biography">
        <el-input v-model="form.biography" type="textarea" :rows="4" />
      </el-form-item>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm">保存</el-button>
        <el-button @click="$router.push('/generals')">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import generalApi from '@/api/general'
import skillApi from '@/api/skill'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)

const isEdit = computed(() => route.params.id !== undefined)

const form = reactive({
  cfgId: null,
  name: '',
  faction: '',
  stars: 3,
  seasonLimit: '全赛季',
  isSP: '否',
  power: 50,
  command: 50,
  intelligence: 50,
  speed: 50,
  politics: 50,
  charm: 50,
  powerGrowth: 0.5,
  commandGrowth: 0.5,
  intelligenceGrowth: 0.5,
  speedGrowth: 0.5,
  politicsGrowth: 0.5,
  charmGrowth: 0.5,
  cavalry: 'C',
  archer: 'C',
  shield: 'C',
  spear: 'C',
  siege: 'C',
  portrait: '',
  innateSkillId: null,
  heritageSkillId: null,
  biography: ''
})

const rules = {
  name: [{ required: true, message: '请输入武将名称', trigger: 'blur' }],
  faction: [{ required: true, message: '请选择阵营', trigger: 'change' }],
  seasonLimit: [{ required: true, message: '请选择赛季限定', trigger: 'change' }],
  isSP: [{ required: true, message: '请选择是否SP', trigger: 'change' }],
  stars: [{ required: true, message: '请选择星级', trigger: 'change' }]
}

// （已改为后端数据获取）

const mockGenerals = [
  {
    cfgId: 1,
    name: '关羽',
    faction: '蜀',
    stars: 5,
    power: 98,
    command: 95,
    intelligence: 80,
    speed: 75,
    politics: 70,
    charm: 90,
    powerGrowth: 0.9,
    commandGrowth: 0.8,
    intelligenceGrowth: 0.6,
    speedGrowth: 0.5,
    politicsGrowth: 0.4,
    charmGrowth: 0.7,
    cavalry: 'S',
    archer: 'C',
    shield: 'B',
    spear: 'A',
    siege: 'C',
    portrait: '',
    innateSkillId: 101,
    biography: '字云长，河东解良人...'
  },
  {
    cfgId: 2,
    name: '诸葛亮',
    faction: '蜀',
    stars: 5,
    power: 65,
    command: 95,
    intelligence: 100,
    speed: 70,
    politics: 95,
    charm: 90,
    powerGrowth: 0.4,
    commandGrowth: 0.8,
    intelligenceGrowth: 1.0,
    speedGrowth: 0.5,
    politicsGrowth: 0.9,
    charmGrowth: 0.7,
    cavalry: 'C',
    archer: 'A',
    shield: 'B',
    spear: 'B',
    siege: 'S',
    portrait: '',
    innateSkillId: 103,
    biography: '字孔明，号卧龙...'
  }
]

const fetchGeneral = async (cfgId) => {
  loading.value = true
  try {
    const res = await generalApi.getGeneral(cfgId)
    if (res) {
      Object.assign(form, res)
    } else {
      ElMessage.warning('未找到对应武将，将使用默认空表单')
    }
  } catch (error) {
    console.error('获取武将信息失败:', error)
    ElMessage.error('获取武将信息失败')
  } finally {
    loading.value = false
  }
}

// 从后端获取战法列表
const skillList = ref([])
const fetchSkills = async () => {
  try {
    const res = await skillApi.getSkills()
    skillList.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('获取战法列表失败:', error)
    ElMessage.error('获取战法列表失败')
  }
}


const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg'
  const isPNG = file.type === 'image/png'
  const isLt8M = file.size / 1024 / 1024 < 8

  if (!isJPG && !isPNG) {
    ElMessage.error('上传头像图片只能是 JPG 或 PNG 格式!')
  }
  if (!isLt8M) {
    ElMessage.error('上传头像图片大小不能超过 8MB!')
  }
  return (isJPG || isPNG) && isLt8M
}

// 立绘上传：编辑直接上传，新增暂存文件，创建成功后补传
const pendingPortraitFile = ref(null)
const handleUpload = async (options) => {
  const file = options.file
  if (form.cfgId) {
    const fd = new FormData()
    fd.append('file', file)
    try {
      const res = await generalApi.uploadPortrait(form.cfgId, fd)
      form.portrait = res?.portrait || form.portrait
      ElMessage.success('立绘上传成功')
    } catch (e) {
      console.error('立绘上传失败:', e)
      ElMessage.error('立绘上传失败')
    }
  } else {
    pendingPortraitFile.value = file
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => {
      form.portrait = reader.result
    }
  }
}

// 技能选择逻辑
const skillDialogVisible = ref(false)
const skillSearch = ref('')
// 使用后端数据填充
// skillList 在上方已声明并由 fetchSkills 填充
const currentSkillType = ref('innate') // 'innate' 或 'heritage'

const openSkillDialog = (type) => {
  currentSkillType.value = type
  skillDialogVisible.value = true
  if (!skillList.value.length) {
    fetchSkills()
  }
}

const filteredSkills = computed(() => {
  const q = skillSearch.value.trim()
  if (!q) return skillList.value
  return skillList.value.filter(s => s.name.includes(q) || String(s.cfgId).includes(q))
})

const onSelectSkill = (row) => {
  if (currentSkillType.value === 'innate') {
    form.innateSkillId = row.cfgId
  } else {
    form.heritageSkillId = row.cfgId
  }
  skillDialogVisible.value = false
}

const skillNameById = (cfgId) => {
  const s = skillList.value.find(x => x.cfgId === cfgId)
  return s ? s.name : '未知战法'
}

const submitForm = async () => {
  if (!formRef.value) return
  
  await formRef.value.validate(async (valid) => {
    if (valid) {
      loading.value = true
      try {
        if (isEdit.value) {
          await generalApi.updateGeneral(form)
          if (pendingPortraitFile.value && form.cfgId) {
            const fd = new FormData()
            fd.append('file', pendingPortraitFile.value)
            const res = await generalApi.uploadPortrait(form.cfgId, fd)
            form.portrait = res?.portrait || form.portrait
          }
          ElMessage.success('更新武将成功')
        } else {
          const created = await generalApi.createGeneral(form)
          if (created?.cfgId) {
            form.cfgId = created.cfgId
          }
          if (pendingPortraitFile.value && form.cfgId) {
            const fd = new FormData()
            fd.append('file', pendingPortraitFile.value)
            const res = await generalApi.uploadPortrait(form.cfgId, fd)
            form.portrait = res?.portrait || form.portrait
          }
          ElMessage.success('添加武将成功')
        }
        router.push('/generals')
      } catch (error) {
        console.error('保存武将失败:', error)
        ElMessage.error('保存武将失败')
      } finally {
        loading.value = false
      }
    }
  })
}

onMounted(() => {
  if (isEdit.value && route.params.id) {
    fetchGeneral(route.params.id)
  }
  fetchSkills()
})
</script>

<style scoped>
.avatar-uploader {
  width: 120px;
  height: 180px; /* 2:3 比例 */
}
.avatar-uploader-icon {
  width: 120px;
  height: 180px; /* 2:3 比例 */
  line-height: 180px;
}
.avatar {
  width: 120px;
  height: 180px; /* 2:3 比例 */
  display: block;
  object-fit: cover;
}
.innate-skill-field {
  display: flex;
  align-items: center;
  gap: 8px;
}
.text-muted { color: #909399; }
.ml8 { margin-left: 8px; }
.mt12 { margin-top: 12px; }

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
  background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Cg fill='%23FFD700'%3E%3Cpath d='M50 5a45 45 0 1 0 0 90c-12.5 0-22.5-10.1-22.5-22.5S37.5 50 50 50s22.5-10.1 22.5-22.5S62.5 5 50 5z'/%3E%3Ccircle cx='62.5' cy='27.5' r='7.5' fill='%23fff2b3'/%3E%3Ccircle cx='37.5' cy='72.5' r='7.5' fill='%23ccad00'/%3E%3C/g%3E%3C/svg%3E");
  filter: drop-shadow(0 1px 0 rgba(0,0,0,0.1));
}
</style>