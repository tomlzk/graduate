<template>
  <div>
    <!-- 模块管理 -->
    <el-card shadow="never">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <h3>模块管理</h3>
          <el-button type="primary" @click="openModuleDialog()">
            <el-icon><Plus /></el-icon> 新增模块
          </el-button>
        </div>
      </template>
      <el-table :data="moduleList" stripe v-loading="moduleLoading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="name" label="模块名称" width="180" />
        <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip />
        <el-table-column label="操作" fixed="right" width="240">
          <template #default="{ row }">
            <el-button size="small" type="primary" @click="openExamInfoSection(row)">考试信息</el-button>
            <el-button size="small" @click="openModuleDialog(row)">编辑</el-button>
            <el-popconfirm title="删除模块将同时删除其下所有内容，确定吗？" @confirm="handleDeleteModule(row.id)">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 考试信息管理 -->
    <el-card shadow="never" style="margin-top:16px" v-if="currentModule">
      <template #header>
        <div style="display:flex;align-items:center;justify-content:space-between">
          <h3>{{ currentModule.name }} - 考试信息管理</h3>
          <el-button type="primary" @click="openExamInfoDialog()">
            <el-icon><Plus /></el-icon> 添加考试信息
          </el-button>
        </div>
      </template>
      <el-table :data="examInfoList" stripe v-loading="examInfoLoading">
        <el-table-column prop="id" label="ID" width="70" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column prop="examTime" label="考试时间" width="160" />
        <el-table-column prop="createTime" label="创建时间" width="180">
          <template #default="{ row }">{{ formatDate(row.createTime) }}</template>
        </el-table-column>
        <el-table-column label="操作" fixed="right" width="160">
          <template #default="{ row }">
            <el-button size="small" @click="openExamInfoDialog(row)">编辑</el-button>
            <el-popconfirm title="确定删除此考试信息吗？" @confirm="handleDeleteExamInfo(row.id)">
              <template #reference>
                <el-button size="small" type="danger">删除</el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        v-if="examInfoTotal > examInfoPageSize"
        layout="total, prev, pager, next"
        :total="examInfoTotal" :page-size="examInfoPageSize"
        v-model:current-page="examInfoPage"
        @current-change="loadExamInfoList"
        style="margin-top:16px;justify-content:flex-end"
      />
    </el-card>

    <!-- 新增/编辑模块弹窗 -->
    <el-dialog v-model="moduleDialogVisible" :title="moduleEditId ? '编辑模块' : '新增模块'" width="500px" destroy-on-close>
      <el-form ref="moduleFormRef" :model="moduleForm" :rules="moduleRules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="moduleForm.name" placeholder="模块名称" maxlength="50" clearable />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="moduleForm.description" type="textarea" :rows="4" placeholder="模块描述" maxlength="500" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="moduleDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="moduleSubmitLoading" @click="handleModuleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑考试信息弹窗 -->
    <el-dialog v-model="examInfoDialogVisible" :title="examInfoEditId ? '编辑考试信息' : '添加考试信息'" width="650px" destroy-on-close>
      <el-form ref="examInfoFormRef" :model="examInfoForm" :rules="examInfoRules" label-width="90px">
        <el-form-item label="标题" prop="title">
          <el-input v-model="examInfoForm.title" placeholder="考试信息标题" maxlength="200" clearable />
        </el-form-item>
        <el-form-item label="考试时间">
          <el-input v-model="examInfoForm.examTime" placeholder="如：2026年6月14日" maxlength="100" clearable />
        </el-form-item>
        <el-form-item label="报名链接">
          <el-input v-model="examInfoForm.registerUrl" placeholder="报名网址" maxlength="500" clearable />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="examInfoForm.content" type="textarea" :rows="8" placeholder="考试信息详细内容" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="examInfoDialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="examInfoSubmitLoading" @click="handleExamInfoSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import {
  adminGetModuleList, createModule, updateModule, deleteModule,
  adminGetExamInfoList, adminAddExamInfo, adminUpdateExamInfo, adminDeleteExamInfo
} from '@/api/admin'
import { ElMessage } from 'element-plus'

// ===== 模块管理 =====
const moduleList = ref([])
const moduleLoading = ref(false)
const moduleDialogVisible = ref(false)
const moduleEditId = ref(null)
const moduleFormRef = ref()
const moduleSubmitLoading = ref(false)
const moduleForm = reactive({ name: '', description: '' })
const moduleRules = {
  name: [{ required: true, message: '请输入模块名称', trigger: 'blur' }]
}

const formatDate = (str) => str ? str.substring(0, 16).replace('T', ' ') : ''

const loadModuleList = async () => {
  moduleLoading.value = true
  try {
    const res = await adminGetModuleList()
    moduleList.value = res.data || []
  } catch (e) {} finally {
    moduleLoading.value = false
  }
}

const openModuleDialog = (row) => {
  if (row) {
    moduleEditId.value = row.id
    moduleForm.name = row.name
    moduleForm.description = row.description || ''
  } else {
    moduleEditId.value = null
    moduleForm.name = ''
    moduleForm.description = ''
  }
  moduleDialogVisible.value = true
}

const handleModuleSubmit = async () => {
  const valid = await moduleFormRef.value.validate().catch(() => false)
  if (!valid) return
  moduleSubmitLoading.value = true
  try {
    if (moduleEditId.value) {
      await updateModule(moduleEditId.value, { name: moduleForm.name, description: moduleForm.description })
      ElMessage.success('修改成功')
    } else {
      await createModule({ name: moduleForm.name, description: moduleForm.description })
      ElMessage.success('创建成功')
    }
    moduleDialogVisible.value = false
    loadModuleList()
  } catch (e) {} finally {
    moduleSubmitLoading.value = false
  }
}

const handleDeleteModule = async (id) => {
  try {
    await deleteModule(id)
    ElMessage.success('已删除')
    if (currentModule.value && currentModule.value.id === id) {
      currentModule.value = null
    }
    loadModuleList()
  } catch (e) {}
}

// ===== 考试信息管理 =====
const currentModule = ref(null)
const examInfoList = ref([])
const examInfoLoading = ref(false)
const examInfoPage = ref(1)
const examInfoPageSize = 10
const examInfoTotal = ref(0)

const examInfoDialogVisible = ref(false)
const examInfoEditId = ref(null)
const examInfoFormRef = ref()
const examInfoSubmitLoading = ref(false)
const examInfoForm = reactive({ title: '', content: '', examTime: '', registerUrl: '' })
const examInfoRules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const openExamInfoSection = (moduleRow) => {
  currentModule.value = moduleRow
  examInfoPage.value = 1
  loadExamInfoList()
}

const loadExamInfoList = async () => {
  if (!currentModule.value) return
  examInfoLoading.value = true
  try {
    const res = await adminGetExamInfoList({
      moduleId: currentModule.value.id,
      page: examInfoPage.value,
      size: examInfoPageSize
    })
    examInfoList.value = res.data?.records || res.data || []
    examInfoTotal.value = res.data?.total || 0
  } catch (e) {} finally {
    examInfoLoading.value = false
  }
}

const openExamInfoDialog = (row) => {
  if (row) {
    examInfoEditId.value = row.id
    examInfoForm.title = row.title
    examInfoForm.content = row.content
    examInfoForm.examTime = row.examTime || ''
    examInfoForm.registerUrl = row.registerUrl || ''
  } else {
    examInfoEditId.value = null
    examInfoForm.title = ''
    examInfoForm.content = ''
    examInfoForm.examTime = ''
    examInfoForm.registerUrl = ''
  }
  examInfoDialogVisible.value = true
}

const handleExamInfoSubmit = async () => {
  const valid = await examInfoFormRef.value.validate().catch(() => false)
  if (!valid) return
  examInfoSubmitLoading.value = true
  try {
    const data = {
      moduleId: currentModule.value.id,
      title: examInfoForm.title,
      content: examInfoForm.content,
      examTime: examInfoForm.examTime,
      registerUrl: examInfoForm.registerUrl
    }
    if (examInfoEditId.value) {
      await adminUpdateExamInfo(examInfoEditId.value, data)
      ElMessage.success('修改成功')
    } else {
      await adminAddExamInfo(data)
      ElMessage.success('添加成功')
    }
    examInfoDialogVisible.value = false
    loadExamInfoList()
  } catch (e) {} finally {
    examInfoSubmitLoading.value = false
  }
}

const handleDeleteExamInfo = async (id) => {
  try {
    await adminDeleteExamInfo(id)
    ElMessage.success('已删除')
    loadExamInfoList()
  } catch (e) {}
}

onMounted(loadModuleList)
</script>
