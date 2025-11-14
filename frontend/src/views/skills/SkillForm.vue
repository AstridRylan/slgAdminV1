<template>
  <div class="container">
    <div class="page-header">
      <h1>{{ isEdit ? '编辑战法' : '添加战法' }}</h1>
    </div>

    <el-form 
      ref="formRef" 
      :model="form" 
      :rules="rules" 
      label-width="120px" 
      class="form-container"
      v-loading="loading">
      
      <el-form-item label="战法名称" prop="name">
        <el-input v-model="form.name" />
      </el-form-item>

      <el-form-item label="战法品质" prop="quality">
        <el-select v-model="form.quality" placeholder="请选择战法品质">
          <el-option label="S" value="S" />
          <el-option label="A" value="A" />
          <el-option label="B" value="B" />
          <el-option label="C" value="C" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="战法立绘" prop="portrait">
        <div class="portrait-upload-container">
          <el-upload
            class="avatar-uploader"
            action="#"
            :show-file-list="false"
            :before-upload="beforePortraitUpload"
            :http-request="handlePortraitUpload">
            <img v-if="form.portrait" :src="form.portrait" class="avatar" />
            <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>
          <el-select v-model="form.portrait" placeholder="选择默认立绘" class="portrait-select" @change="onDefaultPortraitChange">
            <el-option label="兵刃立绘" value="/resources/skin/skill/default_bingren.png" />
            <el-option label="谋略立绘" value="/resources/skin/skill/default_moulue.png" />
            <el-option label="治疗立绘" value="/resources/skin/skill/default_zhiliao.png" />
            <el-option label="增益立绘" value="/resources/skin/skill/default_zengyi.png" />
            <el-option label="减益立绘" value="/resources/skin/skill/default_jianyi.png" />
          </el-select>
        </div>
      </el-form-item>
      
      <el-form-item label="战法类型" prop="triggerType">
        <el-select v-model="form.triggerType" placeholder="请选择战法类型">
          <el-option label="主动" value="主动" />
          <el-option label="突击" value="突击" />
          <el-option label="指挥" value="指挥" />
          <el-option label="被动" value="被动" />
          <el-option label="兵种" value="兵种" />
          <el-option label="阵法" value="阵法" />
          <el-option label="内政" value="内政" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="效果类型" prop="effectTypes">
        <el-checkbox-group v-model="form.effectTypes">
          <el-checkbox label="兵刃">兵刃</el-checkbox>
          <el-checkbox label="谋略">谋略</el-checkbox>
          <el-checkbox label="增益">增益</el-checkbox>
          <el-checkbox label="治疗">治疗</el-checkbox>
          <el-checkbox label="减益">减益</el-checkbox>
        </el-checkbox-group>
      </el-form-item>
      
      <el-form-item label="作用目标" prop="targetType">
        <el-select v-model="form.targetType" placeholder="请选择作用目标">
          <el-option label="自己" value="自己" />
          <el-option label="我军单体" value="我军单体" />
          <el-option label="我军群体（1-2人）" value="我军群体（1-2人）" />
          <el-option label="我军群体（2-3人）" value="我军群体（2-3人）" />
          <el-option label="我军全体" value="我军全体" />
          <el-option label="敌军单体" value="敌军单体" />
          <el-option label="敌军群体（1-2人）" value="敌军群体（1-2人）" />
          <el-option label="敌军群体（2-3人）" value="敌军群体（2-3人）" />
          <el-option label="敌军全体" value="敌军全体" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="可装配" prop="maxEquip">
        <el-input-number v-model="form.maxEquip" :min="1" :max="10" />
      </el-form-item>
      
      <el-form-item label="适配兵种" prop="troopTypes">
        <el-checkbox-group v-model="troopTypes">
          <el-checkbox label="cavalry">骑兵</el-checkbox>
          <el-checkbox label="archer">弓兵</el-checkbox>
          <el-checkbox label="shield">盾兵</el-checkbox>
          <el-checkbox label="spear">枪兵</el-checkbox>
          <el-checkbox label="siege">器械</el-checkbox>
        </el-checkbox-group>
      </el-form-item>

      <el-form-item label="传承出处" prop="heritageSources">
        <div class="heritage-sources">
          <el-tag
            v-for="general in selectedGenerals"
            :key="general.cfgId"
            closable
            @close="removeGeneral(general.cfgId)"
            type="info"
            style="margin-right: 8px; margin-bottom: 8px;"
          >
            {{ general.name }}
          </el-tag>
          <div v-if="selectedGenerals.length === 0" class="text-muted" style="margin-bottom: 0px;">
            未选择传承武将
          </div>
        </div>
        <div style="margin-top: 8px;">
          <el-button size="small" @click="generalDialogVisible = true">添加武将</el-button>
          <el-button size="small" type="danger" @click="clearAllGenerals">清除</el-button>
        </div>
      </el-form-item>

      <el-dialog v-model="generalDialogVisible" title="选择传承武将" width="520px" :close-on-click-modal="false">
        <el-input v-model="generalSearch" placeholder="搜索武将ID或名称" clearable />
        <el-table :data="filteredGenerals" height="320" @row-click="onSelectGeneral" class="mt12">
          <el-table-column prop="cfgId" label="ID" width="100" />
          <el-table-column prop="name" label="名称" />
          <el-table-column prop="faction" label="阵营" width="80" />
        </el-table>
        <template #footer>
          <el-button @click="generalDialogVisible = false">关闭</el-button>
        </template>
      </el-dialog>
      
      <el-form-item label="战法描述" prop="description">
        <el-input v-model="form.description" type="textarea" :rows="4" />
        <div class="description-preview" v-if="form.description">
          <span class="preview-label">预览：</span>
          <span v-html="highlightDescription(form.description)"></span>
        </div>
      </el-form-item>
      
      <el-divider content-position="left">影响因子</el-divider>
      
      <div style="margin-bottom: 15px;">
        <el-button type="primary" size="small" @click="autoCalculateFactors">
          <el-icon></el-icon>
          自动计算
        </el-button>
        <span style="margin-left: 10px; color: #909399; font-size: 12px;">
          请先输入第1级和第10级的数据，然后点击自动计算填充2-9级
        </span>
      </div>
      
      <div class="impact-factors">
        <div v-for="(factor, index) in form.impactFactors" :key="index" class="factor-row">
          <div class="factor-header">
            <span class="level-label">等级{{ index + 1 }}</span>
          </div>
          <div class="factor-content">
            <div class="factor-item">
              <span class="factor-label">发动率：</span>
              <el-input-number 
                v-model="factor.triggerRate" 
                :min="0" 
                :max="100" 
                :step="0" 
                :precision="1"
                :controls="false"
                class="small-input"
              />
              <span class="factor-unit">%</span>
            </div>
            <div class="factor-item">
              <span class="factor-label">数值系数：</span>
              <div class="coefficient-list">
                <el-input-number 
                  v-for="(coeff, coeffIndex) in factor.coefficients" 
                  :key="coeffIndex"
                  v-model="factor.coefficients[coeffIndex]"
                  :min="0" 
                  :max="1000" 
                  :step="1"
                  :precision="1"
                  :controls="false"
                  class="coefficient-input"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <el-form-item>
        <el-button type="primary" @click="submitForm">保存</el-button>
        <el-button @click="$router.push('/skills')">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.container {
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.form-container {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  max-width: 800px;
}

.portrait-upload-container {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar-uploader {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  width: 120px;
  height: 180px; /* 2:3 比例 */
}

.avatar-uploader:hover {
  border-color: #409eff;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 120px;
  height: 180px; /* 2:3 比例 */
  text-align: center;
  line-height: 180px;
}

.avatar {
  width: 120px;
  height: 180px; /* 2:3 比例 */
  display: block;
  object-fit: cover;
}

.portrait-select {
  width: 200px;
}

.description-preview {
  margin-top: 10px;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.5;
}

.preview-label {
  color: #909399;
  font-weight: bold;
  margin-right: 8px;
}

.impact-factors {
  margin: 20px 0;
}

.factor-row {
  display: flex;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background: #f5f7fa;
  border-radius: 6px;
  border: 1px solid #e4e7ed;
}

.factor-header {
  width: 80px;
  text-align: center;
}

.level-label {
  font-weight: bold;
  color: #303133;
  font-size: 16px;
}

.factor-content {
  flex: 1;
  display: flex;
  gap: 30px;
  align-items: center;
}

.factor-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.factor-label {
  font-weight: 500;
  color: #606266;
  white-space: nowrap;
}

.factor-unit {
  color: #909399;
  font-size: 12px;
}

.small-input {
  width: 60px !important;
}

.coefficient-list {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.coefficient-input {
  width: 70px !important;
}

.heritage-sources {
  display: flex;
  flex-wrap: nowrap;
  align-items: center;
  min-height: 20px;
  padding: 3px;
  border: 1px solid #dcdfe6;
  border-radius: 1px;
  background-color: #f5f7fa;
}

.text-muted {
  color: #909399;
  font-size: 13px;
}

.el-checkbox-group {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.el-divider {
  margin: 30px 0;
}
</style>

<script setup>
import { ref, onMounted, reactive, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import skillApi from '@/api/skill'
import generalApi from '@/api/general'

const route = useRoute()
const router = useRouter()
const formRef = ref(null)
const loading = ref(false)
const skillDialogVisible = ref(false)
const generalDialogVisible = ref(false)
const generalSearch = ref('')
const selectedGenerals = ref([])

const isEdit = computed(() => route.params.id !== undefined)

const form = reactive({
  cfgId: null,
  name: '',
  portrait: '',
  triggerType: '',
  effectTypes: [],
  targetType: '',
  maxEquip: 1,
  cavalry: false,
  archer: false,
  shield: false,
  spear: false,
  siege: false,
  heritageSources: [], // 传承出处
  description: '',
  impactFactors: []
})

const troopTypes = computed({
  get() {
    const types = [];
    if (form.cavalry) types.push('cavalry');
    if (form.archer) types.push('archer');
    if (form.shield) types.push('shield');
    if (form.spear) types.push('spear');
    if (form.siege) types.push('siege');
    return types;
  },
  set(newVal) {
    form.cavalry = newVal.includes('cavalry');
    form.archer = newVal.includes('archer');
    form.shield = newVal.includes('shield');
    form.spear = newVal.includes('spear');
    form.siege = newVal.includes('siege');
  }
});

// 监听描述变化，更新影响因子参数数量
watch(() => form.description, (newVal) => {
  updateImpactFactors(newVal)
})

// 计算占位符数量
const countPlaceholders = (description) => {
  if (!description) return 0
  const matches = description.match(/%[df]/g)
  return matches ? matches.length : 0
}

// 更新影响因子
const updateImpactFactors = (description) => {
  const placeholderCount = countPlaceholders(description)
  
  // 初始化或更新影响因子
  if (form.impactFactors.length === 0) {
    // 初始化10个等级，每个等级的发动率递增
    for (let i = 0; i < 10; i++) {
      form.impactFactors.push({
        triggerRate: 35, // 从35%开始，每个等级增加5%
        coefficients: new Array(placeholderCount).fill(100)
      })
    }
  } else {
    // 更新现有影响因子的参数数量
    form.impactFactors.forEach((factor, index) => {
      const currentLength = factor.coefficients.length
      if (currentLength < placeholderCount) {
        // 添加缺少的参数
        for (let i = currentLength; i < placeholderCount; i++) {
          factor.coefficients.push(100)
        }
      } else if (currentLength > placeholderCount) {
        // 删除多余的参数
        factor.coefficients.splice(placeholderCount)
      }
    })
  }
}

// 高亮描述中的占位符
const highlightDescription = (description) => {
  if (!description) return ''
  return description.replace(/(%[df])/g, '<span style="color: #67c23a; font-weight: bold;">$1</span>')
}

const rules = {
  name: [{ required: true, message: '请输入战法名称', trigger: 'blur' }],
  portrait: [{ required: false, message: '请上传战法立绘', trigger: 'change' }],
  triggerType: [{ required: true, message: '请选择触发类型', trigger: 'change' }],
  targetType: [{ required: true, message: '请选择作用目标', trigger: 'change' }],
  description: [{ required: true, message: '请输入战法描述', trigger: 'blur' }]
}

// 模拟数据
const mockSkills = [
  {
    cfgId: 1,
    name: '威震华夏',
    cavalry: true,
    archer: false,
    shield: false,
    spear: true,
    siege: false,
    effectTypes: ['兵刃', '增益'],
    targetType: '敌军单体',
    maxEquip: 1,
    heritageSources: [1, 5],
    description: '对敌军单体造成%d点兵刃伤害，并有%f概率使自身获得增益状态，持续2回合。',
    impactFactors: [
      { triggerRate: 35, coefficients: [100, 50] },
      { triggerRate: 40, coefficients: [110, 55] },
      { triggerRate: 45, coefficients: [120, 60] },
      { triggerRate: 50, coefficients: [130, 65] },
      { triggerRate: 55, coefficients: [140, 70] },
      { triggerRate: 60, coefficients: [150, 75] },
      { triggerRate: 65, coefficients: [160, 80] },
      { triggerRate: 70, coefficients: [170, 85] },
      { triggerRate: 75, coefficients: [180, 90] },
      { triggerRate: 80, coefficients: [200, 100] }
    ]
  }
]

const mockGenerals = [
  { cfgId: 100001, name: '关羽', faction: '蜀' },
  { cfgId: 100002, name: '张飞', faction: '蜀' },
  { cfgId: 100003, name: '诸葛亮', faction: '蜀' },
  { cfgId: 100004, name: '刘备', faction: '蜀' },
  { cfgId: 100005, name: '曹操', faction: '魏' },
  { cfgId: 100006, name: '司马懿', faction: '魏' },
  { cfgId: 100007, name: '孙权', faction: '吴' },
  { cfgId: 100008, name: '周瑜', faction: '吴' }
]

// 后端武将列表
const generalList = ref([])
const fetchGenerals = async () => {
  try {
    const res = await generalApi.getGenerals();
    generalList.value = Array.isArray(res) ? res : [];
    // 如果此时form中已有传承数据，则更新selectedGenerals
    if (form.heritageSources && form.heritageSources.length > 0) {
      updateSelectedGenerals(form.heritageSources);
    }
  } catch (error) {
    console.error('获取武将列表失败:', error);
    ElMessage.error('获取武将列表失败');
  }
};

const fetchSkill = async (cfgId) => {
  loading.value = true;
  try {
    const res = await skillApi.getSkill(cfgId);
    Object.assign(form, res);

    // 预选传承武将
    if (res.heritageSources && generalList.value.length) {
      updateSelectedGenerals(res.heritageSources);
    }

  } catch (error) {
    console.error('获取战法信息失败:', error);
    ElMessage.error('获取战法信息失败');
  } finally {
    loading.value = false;
  }
};

const updateSelectedGenerals = (sources) => {
  if (!Array.isArray(sources)) return;

  selectedGenerals.value = sources.map(source => {
    let cfgId;
    if (typeof source === 'object' && source !== null) {
      cfgId = Object.keys(source)[0];
    } else {
      cfgId = source;
    }
    const general = generalList.value.find(g => g.cfgId == cfgId);
    return general ? { cfgId: general.cfgId, name: general.name } : null;
  }).filter(g => g !== null);
};

// 图片上传处理
const handleImageSuccess = (response, file) => {
  form.portrait = URL.createObjectURL(file.raw)
}

const beforePortraitUpload = (file) => {
  const isImage = file.type.startsWith('image/')
  const isLt8M = file.size / 1024 / 1024 < 8
  
  if (!isImage) {
    ElMessage.error('只能上传图片文件!')
  }
  if (!isLt8M) {
    ElMessage.error('图片大小不能超过 8MB!')
  }
  return isImage && isLt8M
}

// 立绘上传：编辑直接上传，新增暂存文件，创建成功后补传
const pendingPortraitFile = ref(null)
const handlePortraitUpload = async (options) => {
  const file = options.file
  if (form.cfgId) {
    const fd = new FormData()
    fd.append('file', file)
    try {
      const res = await skillApi.uploadPortrait(form.cfgId, fd)
      form.portrait = res?.portrait || form.portrait
      ElMessage.success('立绘上传成功')
    } catch (e) {
      ElMessage.error('立绘上传失败')
    }
  } else {
    pendingPortraitFile.value = file
    const reader = new FileReader()
    reader.onload = (e) => {
      // 仅用于前端预览，避免将base64保存到JSON
      form.portrait = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const onDefaultPortraitChange = (value) => {
  form.portrait = value
}

// 自动计算影响因子
const autoCalculateFactors = () => {
  if (form.impactFactors.length < 10) {
    ElMessage.warning('请先确保有完整的10个等级数据')
    return
  }
  
  const firstLevel = form.impactFactors[0] // 第1级
  const tenthLevel = form.impactFactors[9]   // 第10级
  
  // 计算第2-9级的数据（索引1-8）
  for (let i = 1; i <= 8; i++) {
    const currentLevel = form.impactFactors[i]
    
    // 计算发动率（线性插值）
    const triggerRateStep = (tenthLevel.triggerRate - firstLevel.triggerRate) / 9
    currentLevel.triggerRate = Number((firstLevel.triggerRate + triggerRateStep * i).toFixed(1))
    
    // 计算每个系数（线性插值）
    for (let j = 0; j < currentLevel.coefficients.length; j++) {
      if (j < firstLevel.coefficients.length && j < tenthLevel.coefficients.length) {
        const coeffStep = (tenthLevel.coefficients[j] - firstLevel.coefficients[j]) / 9
        currentLevel.coefficients[j] = Number((firstLevel.coefficients[j] + coeffStep * i).toFixed(1))
      }
    }
  }
  
  ElMessage.success('自动计算完成，2-9级数据已填充')
}

// 传承出处相关函数
const filteredGenerals = computed(() => {
  const q = generalSearch.value.trim()
  const list = generalList.value.length ? generalList.value : []
  if (!q) return list
  return list.filter(g => 
    g.name?.includes(q) || 
    String(g.cfgId).includes(q) ||
    g.faction?.includes(q)
  )
})

const onSelectGeneral = (row) => {
  // 检查是否已经添加过
  if (selectedGenerals.value.find(g => g.cfgId === row.cfgId)) {
    ElMessage.warning('该武将已在传承出处中')
    return
  }
  
  selectedGenerals.value.push({
    cfgId: row.cfgId,
    name: row.name,
    faction: row.faction
  })
  generalDialogVisible.value = false
  generalSearch.value = ''
}

const removeGeneral = (cfgId) => {
  const index = selectedGenerals.value.findIndex(g => g.cfgId === cfgId)
  if (index > -1) {
    selectedGenerals.value.splice(index, 1)
  }
}

const clearAllGenerals = () => {
  selectedGenerals.value = []
  ElMessage.success('已清除所有传承武将')
}
  

const submitForm = async () => {
  if (!formRef.value) return
  
await formRef.value.validate(async (valid) => {
    if (valid) {
        loading.value = true
        try {
          // 准备提交数据
          let submitData = {
            ...form,
            heritageSources: selectedGenerals.value.map(g => ({ [g.cfgId]: g.name })) // 修改为[{id:name}]格式
          };
          // 新增且存在待上传自定义立绘时，避免保存base64
          if (!form.cfgId && pendingPortraitFile.value) {
            submitData.portrait = ''
          }
          
          if (isEdit.value) {
            await skillApi.updateSkill(submitData)
            ElMessage.success('修改成功')
          } else {
            const created = await skillApi.createSkill(submitData)
            if (created?.cfgId) {
              form.cfgId = created.cfgId
              if (pendingPortraitFile.value) {
                const fd = new FormData()
                fd.append('file', pendingPortraitFile.value)
                const res = await skillApi.uploadPortrait(form.cfgId, fd)
                form.portrait = res?.portrait || form.portrait
              }
            }
            ElMessage.success('添加成功')
          }
          
          router.push('/skills')
        } catch (error) {
        ElMessage.error(isEdit.value ? '修改失败' : '添加失败')
      } finally {
        loading.value = false
      }
    }
  })
}

onMounted(() => {
  if (isEdit.value && route.params.id) {
    fetchSkill(route.params.id)
  }
  fetchGenerals()
})
</script>