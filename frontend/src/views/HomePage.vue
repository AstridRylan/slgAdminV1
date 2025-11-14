<template>
  <div class="container">
    <h1 class="page-header">欢迎使用SLG后台管理系统</h1>
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>武将管理</span>
              <el-button class="button" type="primary" @click="$router.push('/generals')">查看详情</el-button>
            </div>
          </template>
          <div class="card-content">
            <p>管理游戏中的武将信息，包括基本属性、技能、兵种适应性等。</p>
            <ul>
              <li>查看武将列表</li>
              <li>添加新武将</li>
              <li>编辑武将信息</li>
              <li>删除武将</li>
            </ul>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>战法管理</span>
              <el-button class="button" type="primary" @click="$router.push('/skills')">查看详情</el-button>
            </div>
          </template>
          <div class="card-content">
            <p>管理游戏中的战法信息，包括战法名称、适配兵种、效果描述等。</p>
            <ul>
              <li>查看战法列表</li>
              <li>添加新战法</li>
              <li>编辑战法信息</li>
              <li>删除战法</li>
            </ul>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
// 首页逻辑
</script>