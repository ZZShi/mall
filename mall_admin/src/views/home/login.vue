<template>
    <el-row class="login-container">
        <el-col :lg="16" :md="12" class="left">
            <div>
                <div>欢迎光临</div>
                <div>基于 VUE3 + Vite 的学习地址登录页</div>
            </div>
        </el-col>
        <el-col :lg="8" :md="12" class="right">
            <h2 class="title">欢迎回来</h2>
            <div>
                <span class="line"></span>
                <span>账号密码登录</span>
                <span class="line"></span>
            </div>
            <div>
                <el-form :model="form" class="w-[250px]">
                    <el-form-item>
                        <el-input v-model="form.username" placeholder="请输入用户名">
                            <template #prefix>
                                <el-icon><user /></el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-input v-model="form.password" placeholder="请输入密码" type="password" show-password>
                            <template #prefix>
                                <el-icon><lock /></el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button round color="#626aef" class="w-[250px]" type="primary" @click="onSubmit">登 录</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-col>
    </el-row> 
</template>

<script lang="ts" setup>
import { reactive } from 'vue'

const form = reactive({
    username: '',
    password: '',
})

const onSubmit = () => {
  console.log('submit!')
}

</script>

<style scoped>
.login-container {
    @apply  min-h-screen bg-indigo-500;
}
.login-container .left, .login-container .right {
    @apply flex items-center justify-center;
}
.login-container .right {
    @apply  bg-light-50 flex-col;
}
.left>div>div:first-child {
    @apply font-bold text-5xl text-light-50 mb-4;
}
.left>div>div:last-child {
    @apply  text-gray-200 text-sm;
}
.right .title {
    @apply font-bold text-3xl text-gray-800;
}
.right>div {
    @apply flex items-center justify-center my-5 text-gray-300 space-x-2;
}
.right .line {
    @apply h-[1px] w-16 bg-gray-200;
}

</style>