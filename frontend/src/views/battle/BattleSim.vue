<template>
  <div class="container">
    <div class="page-header">
      <h1>模拟战斗</h1>
    </div>
    <div class="battle-layout">
      <div class="team team-left">
        <div class="general-card" v-for="(g, idx) in team1.generals" :key="idx">
          <div class="top-row">
            <el-button class="switch-btn" size="small" @click="openGeneralDialog('team1', idx)">切换武将</el-button>
            <el-tag :type="team1.chiefIndex === idx ? 'danger' : 'info'">{{ team1.chiefIndex === idx ? '主将' : '副将' }}</el-tag>
          </div>
          <div class="portrait-box">
            <img :src="g.portrait || defaultGeneral" class="portrait" />
            <span class="badge faction">{{ g.faction || '-' }}</span>
            <div class="portrait-overlay">
              <div class="portrait-name">{{ g.name || '-' }}</div>
              <div class="portrait-stars">
                <span v-for="n in (g.stars || 0)" :key="n" class="star">★</span>
              </div>
            </div>
          </div>
          <div class="skills">
            <el-button class="skill-btn" :class="{ selected: !!g.innateSkillId, unselected: !g.innateSkillId }">{{ skillNameById(g.innateSkillId) || '自带战法' }}</el-button>
            <div class="skill-row">
              <el-button class="skill-btn" :class="{ selected: g.skills[1], unselected: !g.skills[1] }" @click="openSkillDialog('team1', idx, 1)">{{ (g.skills[1] && g.skills[1].name) || '选择战法' }}</el-button>
            </div>
            <div class="skill-row">
              <el-button class="skill-btn" :class="{ selected: g.skills[2], unselected: !g.skills[2] }" @click="openSkillDialog('team1', idx, 2)">{{ (g.skills[2] && g.skills[2].name) || '选择战法' }}</el-button>
            </div>
          </div>
        </div>
      </div>
      <div class="vs">VS</div>
      <div class="team team-right">
        <div class="general-card" v-for="(g, idx) in team2.generals" :key="idx">
          <div class="top-row">
            <el-button class="switch-btn" size="small" @click="openGeneralDialog('team2', idx)">切换武将</el-button>
            <el-tag :type="team2.chiefIndex === idx ? 'danger' : 'info'">{{ team2.chiefIndex === idx ? '主将' : '副将' }}</el-tag>
          </div>
          <div class="portrait-box">
            <img :src="g.portrait || defaultGeneral" class="portrait" />
            <span class="badge faction">{{ g.faction || '-' }}</span>
            <div class="portrait-overlay">
              <div class="portrait-name">{{ g.name || '-' }}</div>
              <div class="portrait-stars">
                <span v-for="n in (g.stars || 0)" :key="n" class="star">★</span>
              </div>
            </div>
          </div>
          <div class="skills">
            <el-button class="skill-btn" :class="{ selected: !!g.innateSkillId, unselected: !g.innateSkillId }" >{{ skillNameById(g.innateSkillId) || '自带战法' }}</el-button>
            <div class="skill-row">
              <el-button class="skill-btn" :class="{ selected: g.skills[1], unselected: !g.skills[1] }" @click="openSkillDialog('team2', idx, 1)">{{ (g.skills[1] && g.skills[1].name) || '选择战法' }}</el-button>
            </div>
            <div class="skill-row">
              <el-button class="skill-btn" :class="{ selected: g.skills[2], unselected: !g.skills[2] }" @click="openSkillDialog('team2', idx, 2)">{{ (g.skills[2] && g.skills[2].name) || '选择战法' }}</el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <el-dialog v-model="skillDialogVisible" title="选择战法" width="700px">
      <el-input v-model="skillSearch" placeholder="搜索名称或ID" style="margin-bottom:8px;" />
      <el-table :data="filteredSkills" height="360">
        <el-table-column prop="name" label="名称" width="160" />
        <el-table-column prop="triggerType" label="类型" width="100" />
        <el-table-column label="效果" width="160">
          <template #default="scope">
            {{ Array.isArray(scope.row.effectTypes) ? scope.row.effectTypes.join(' / ') : '' }}
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" />
        <el-table-column label="选择" width="100">
          <template #default="scope">
            <el-button type="primary" size="small" @click="chooseSkill(scope.row)">选择</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <el-dialog v-model="generalDialogVisible" title="选择武将" width="700px">
      <el-input v-model="generalSearch" placeholder="搜索名称或ID" style="margin-bottom:8px;" />
      <el-table :data="filteredGenerals" height="360">
        <el-table-column label="立绘" width="100">
          <template #default="scope">
            <el-image :src="scope.row.portrait || defaultGeneral" style="width:64px;height:96px;border-radius:6px;" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="名称" width="120" />
        <el-table-column prop="faction" label="阵营" width="100" />
        <el-table-column label="星级" width="120">
          <template #default="scope">
            <el-rate v-model="scope.row.stars" disabled :max="5" />
          </template>
        </el-table-column>
        <el-table-column label="自带战法" width="160">
          <template #default="scope">
            <el-tag type="warning">{{ skillNameById(scope.row.innateSkillId) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="选择" width="100">
          <template #default="scope">
            <el-button type="primary" size="small" @click="chooseGeneral(scope.row)">选择</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>
    <div style="margin-top:16px;display:flex;gap:12px;align-items:center;">
      <el-select v-model="team1.chiefIndex" placeholder="队伍一主将位置">
        <el-option :label="'最左(0)'" :value="0" />
        <el-option :label="'中间(1)'" :value="1" />
        <el-option :label="'最右(2)'" :value="2" />
      </el-select>
      <el-select v-model="team2.chiefIndex" placeholder="队伍二主将位置">
        <el-option :label="'最左(0)'" :value="0" />
        <el-option :label="'中间(1)'" :value="1" />
        <el-option :label="'最右(2)'" :value="2" />
      </el-select>
      <el-button type="primary" @click="startBattle">开始战斗</el-button>
    </div>
    <el-card class="box-card" style="margin-top:16px;">
      <template #header>
        <div class="card-header">
          <span>战报</span>
          <div class="round-tabs" v-if="battleLog.length">
            <el-button
              v-for="r in totalRounds"
              :key="r"
              size="small"
              class="round-tab"
              :class="{ active: currentRound === r }"
              @click="scrollToRound(r)"
            >回合{{ r }}</el-button>
          </div>
        </div>
      </template>
      <div class="log" ref="logRef" @scroll="onLogScroll">
        <div class="log-item" v-for="(e,i) in battleLog" :key="i" :data-index="i">
          <span>回合{{ e.round }} - {{ e.phase }}：{{ e.attacker }} → {{ e.defender }}，{{ e.triggered ? '触发' : '未触发' }}，伤害 {{ e.damage }}</span>
        </div>
      </div>
      <div class="result" v-if="result">
        <p>胜者：{{ result.winner }}</p>
        <p>队伍一兵力：{{ result.finalTroops.team1.join(', ') }}</p>
        <p>队伍二兵力：{{ result.finalTroops.team2.join(', ') }}</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import generalApi from '@/api/general'
import skillApi from '@/api/skill'
import battleApi from '@/api/battle'
import { ElMessage } from 'element-plus'

const defaultGeneral = '/resources/skin/skill/default_bingren.png'
const skills = ref([])
const battleLog = ref([])
const result = ref(null)
const logRef = ref(null)
const currentRound = ref(1)
const totalRounds = computed(() => {
  const rounds = new Set((battleLog.value || []).map(e => e.round))
  return Array.from(rounds).sort((a,b) => a-b)
})

const roundAnchors = ref([])
const initRoundAnchors = () => {
  roundAnchors.value = []
  const container = logRef.value
  if (!container) return
  const items = container.querySelectorAll('.log-item')
  const firstIndexByRound = new Map()
  battleLog.value.forEach((e, idx) => {
    if (!firstIndexByRound.has(e.round)) firstIndexByRound.set(e.round, idx)
  })
  totalRounds.value.forEach(r => {
    const idx = firstIndexByRound.get(r)
    if (idx !== undefined) roundAnchors.value[r] = items[idx]
  })
}

const scrollToRound = (r) => {
  const container = logRef.value
  const anchor = roundAnchors.value[r]
  if (!container || !anchor) return
  const top = anchor.getBoundingClientRect().top - container.getBoundingClientRect().top + container.scrollTop
  container.scrollTo({ top, behavior: 'smooth' })
  currentRound.value = r
}

const onLogScroll = () => {
  const container = logRef.value
  if (!container) return
  const scrollTop = container.scrollTop
  let active = currentRound.value
  totalRounds.value.forEach(r => {
    const el = roundAnchors.value[r]
    if (!el) return
    const top = el.getBoundingClientRect().top - container.getBoundingClientRect().top + container.scrollTop
    if (scrollTop >= top - 1) active = r
  })
  currentRound.value = active
}
const skillNameById = (id) => {
  const s = skills.value.find(x => x.cfgId === id)
  return s ? s.name : (id || '')
}

const team1 = ref({
  chiefIndex: 0,
  generals: [ { skills: [null,null,null] }, { skills: [null,null,null] }, { skills: [null,null,null] } ]
})
const team2 = ref({
  chiefIndex: 2,
  generals: [ { skills: [null,null,null] }, { skills: [null,null,null] }, { skills: [null,null,null] } ]
})

const allGenerals = ref([])
const generalDialogVisible = ref(false)
const targetTeam = ref('team1')
const targetIndex = ref(0)
const generalSearch = ref('')
const filteredGenerals = computed(() => {
  const q = generalSearch.value.trim()
  if (!q) return allGenerals.value
  return allGenerals.value.filter(g => (g.name || '').includes(q) || String(g.cfgId || '').includes(q))
})

const fillGenerals = async () => {
  try {
    const gs = await generalApi.getGenerals()
    allGenerals.value = Array.isArray(gs) ? gs : []
    const indices = Array.from({ length: allGenerals.value.length }, (_, i) => i)
    for (let i = indices.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1))
      const t = indices[i]; indices[i] = indices[j]; indices[j] = t
    }
    const team1Idx = indices.slice(0, Math.min(3, indices.length))
    const team2Idx = indices.slice(Math.min(3, indices.length), Math.min(6, indices.length))
    const pick = (i) => {
      const g = allGenerals.value[i] || {}
      return { ...g, skills: [null,null,null] }
    }
    team1.value.generals = team1Idx.map(pick)
    team2.value.generals = (team2Idx.length ? team2Idx : team1Idx).map(pick)
  } catch {}
}

const fillSkills = async () => {
  try {
    const res = await skillApi.getSkills()
    skills.value = Array.isArray(res) ? res : []
  } catch {}
}

const startBattle = async () => {
  try {
    const payload = { team1: team1.value, team2: team2.value }
    const res = await battleApi.simulate(payload)
    battleLog.value = res.log || []
    result.value = res
    await nextTick()
    initRoundAnchors()
    scrollToRound(1)
  } catch (e) {
    ElMessage.error('战斗计算失败')
  }
}

const openGeneralDialog = (team, idx) => {
  targetTeam.value = team
  targetIndex.value = idx
  generalDialogVisible.value = true
}

const chooseGeneral = (row) => {
  const obj = { ...row, skills: [null, null, null] }
  if (targetTeam.value === 'team1') {
    team1.value.generals[targetIndex.value] = obj
  } else {
    team2.value.generals[targetIndex.value] = obj
  }
  generalDialogVisible.value = false
}

const skillDialogVisible = ref(false)
const skillSearch = ref('')
const skillTargetTeam = ref('team1')
const skillTargetIndex = ref(0)
const skillTargetPos = ref(1)
const filteredSkills = computed(() => {
  const q = skillSearch.value.trim()
  if (!q) return skills.value
  return skills.value.filter(s => (s.name || '').includes(q) || String(s.cfgId || '').includes(q))
})

const openSkillDialog = (team, idx, pos) => {
  skillTargetTeam.value = team
  skillTargetIndex.value = idx
  skillTargetPos.value = pos
  skillDialogVisible.value = true
}

const chooseSkill = (row) => {
  const obj = { cfgId: row.cfgId, name: row.name }
  if (skillTargetPos.value === 0) {
    if (skillTargetTeam.value === 'team1') {
      team1.value.generals[skillTargetIndex.value].innateSkillId = obj.cfgId
    } else {
      team2.value.generals[skillTargetIndex.value].innateSkillId = obj.cfgId
    }
  } else {
    if (skillTargetTeam.value === 'team1') {
      team1.value.generals[skillTargetIndex.value].skills[skillTargetPos.value] = obj
    } else {
      team2.value.generals[skillTargetIndex.value].skills[skillTargetPos.value] = obj
    }
  }
  skillDialogVisible.value = false
}

onMounted(() => {
  fillGenerals()
  fillSkills()
})
</script>

<style scoped>
.battle-layout {
  display: grid;
  grid-template-columns: 1fr 80px 1fr;
  gap: 16px;
  align-items: start;
}
.team {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}
.team-right { flex-direction: row-reverse; }
.general-card { width: 160px; }
.portrait-box { position: relative; }
.portrait { width: 120px; height: 180px; object-fit: cover; border-radius: 6px; }
.portrait-overlay { position: absolute; left: 0; bottom: 6px; width: 120px; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.portrait-name { background: rgba(0,0,0,0.5); color: #fff; padding: 2px 6px; border-radius: 4px; font-size: 12px; text-align: center; max-width: 100%; }
.portrait-stars { display: flex; justify-content: center; }
.portrait-stars .star { color: #fadb14; font-size: 14px; margin: 0 1px; }
.badge { position: absolute; padding: 2px 6px; border-radius: 4px; background: rgba(0,0,0,0.6); color:#fff; font-size: 12px; }
.badge.faction { left: 6px; top: 6px; }
.badge.stars { left: 6px; bottom: 6px; }
.skills { margin-top: 8px; display: grid; gap: 6px; }
.vs { font-size: 32px; font-weight: 800; display:flex; align-items:center; justify-content:center; }
.log { max-height: 240px; overflow:auto; font-size: 13px; }
.log-item { padding: 4px 0; border-bottom: 1px dashed #eee; }
.card-header { display:flex; align-items:center; justify-content: space-between; }
.round-tabs { display:flex; gap:6px; }
.round-tab { padding: 2px 8px; }
.round-tab.active { background-color:#409eff !important; color:#fff !important; }
.top-row { display:flex; align-items:center; gap:8px; margin-bottom: 6px; }
.skill-row { margin-top: 6px; }
.skill-btn { width: 120px; border-radius: 4px; font-size: 13px; }
.skill-btn.selected { background-color: #fff7e6 !important; border-color: #ffd591 !important; color: #ad6800 !important; }
.skill-btn.unselected { background-color: #f5f5f5 !important; border-color: #d9d9d9 !important; color: #606266 !important; }
.skill-pill { padding: 6px 8px; border-radius: 4px; font-size: 13px; }
.skill-pill.innate { background: #fff7e6; border: 1px solid #ffd591; color: #ad6800; }
.switch-btn { margin-bottom: 0; }
</style>
const logRef = ref(null)
const currentRound = ref(1)
const totalRounds = computed(() => {
  const rounds = new Set((battleLog.value || []).map(e => e.round))
  return Array.from(rounds).sort((a,b) => a-b)
})

const roundAnchors = ref([])
const initRoundAnchors = () => {
  roundAnchors.value = []
  const container = logRef.value
  if (!container) return
  const items = container.querySelectorAll('.log-item')
  const firstIndexByRound = new Map()
  // 根据数据计算每个回合的首行索引
  battleLog.value.forEach((e, idx) => {
    if (!firstIndexByRound.has(e.round)) firstIndexByRound.set(e.round, idx)
  })
  totalRounds.value.forEach(r => {
    const idx = firstIndexByRound.get(r)
    if (idx !== undefined) roundAnchors.value[r] = items[idx]
  })
}

const scrollToRound = (r) => {
  const container = logRef.value
  const anchor = roundAnchors.value[r]
  if (!container || !anchor) return
  const firstItem = container.querySelector('.log-item')
  const top = anchor.getBoundingClientRect().top - container.getBoundingClientRect().top + container.scrollTop
  container.scrollTo({ top, behavior: 'smooth' })
  currentRound.value = r
}

const onLogScroll = () => {
  const container = logRef.value
  if (!container) return
  const scrollTop = container.scrollTop
  let active = currentRound.value
  totalRounds.value.forEach(r => {
    const el = roundAnchors.value[r]
    if (!el) return
    const top = el.getBoundingClientRect().top - container.getBoundingClientRect().top + container.scrollTop
    if (scrollTop >= top - 1) active = r
  })
  currentRound.value = active
}
