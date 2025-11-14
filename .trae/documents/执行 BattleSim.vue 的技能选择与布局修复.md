## 目标
- 修复技能装配报错并优化交互，满足按钮+弹窗选择战法、顶部同排对齐的要求。

## 具体修改
### 模板更新（BattleSim.vue）
1. 武将卡顶部：为每张卡增加 `top-row` 容器，包含：
   - 左侧 `el-button`：切换武将（调用 `openGeneralDialog('teamX', idx)`）
   - 右侧 `el-tag`：显示“主将/副将”（根据 `chiefIndex` 判断）
2. 自带战法显示：将原 `el-input` 改为只读色块 `<div class="skill-pill innate">{{ skillNameById(g.innateSkillId) || '自带战法' }}</div>`。
3. 选择战法按钮：将原 `el-select` 改为单按钮：
   - `<el-button class="skill-btn" :type="g.skills[pos] ? 'primary' : 'default'" :plain="!g.skills[pos]" @click="openSkillDialog('teamX', idx, pos)">{{ (g.skills[pos] && g.skills[pos].name) || '选择战法' }}</el-button>`
   - 两个按钮分别对应第二、第三战法位（pos=1/2）。
4. 新增“选择战法”弹窗：`<el-dialog v-model="skillDialogVisible" title="选择战法">`，表格列：名称、类型、效果、描述，行尾“选择”按钮调用 `chooseSkill(row)`。

### 脚本更新（<script setup>）
- 保留原有 `openGeneralDialog/chooseGeneral`。
- 新增状态：`skillDialogVisible`、`skillSearch`、`skillTargetTeam`、`skillTargetIndex`、`skillTargetPos`。
- 新增计算：`filteredSkills = computed(() => skills 按名称/ID过滤)`。
- 新增方法：
  - `openSkillDialog(team, idx, pos)`：记录目标并打开弹窗
  - `chooseSkill(row)`：将 `{cfgId, name}` 写入 `teamX.generals[idx].skills[pos]`，关闭弹窗

### 样式更新（<style scoped>）
- `.top-row { display:flex; align-items:center; gap:8px; margin-bottom:6px; }`
- `.skill-row { margin-top:6px; }`
- `.skill-btn { width:100%; }`
- `.skill-pill { padding:6px 8px; border-radius:4px; font-size:13px; }`
- `.skill-pill.innate { background:#fff7e6; border:1px solid #ffd591; color:#ad6800; }`
- `.switch-btn { margin-bottom:0; }`

## 验证
- 点击技能按钮弹出战法选择弹窗，无控制台错误。
- 未选择时按钮显示“选择战法”（灰色）；选择后显示技能名并高亮。
- 自带战法显示为色块；“切换武将”与“主将/副将”同排对齐。

确认后我将直接在 BattleSim.vue 中实施上述模板、脚本与样式修改并提交。