<template>
    <el-row class="login-container">
        <el-col :lg="16" :md="12" class="left">
            <div>
                <!-- <div>淘宝商城</div>
                <div>基于 VUE3 + Vite 的学习地址登录页</div> -->
                <!-- <el-image style="width: 100px; height: 100px" :src="https://vuejs.org/guide/quick-start.html#local"></el-image> -->
            </div>
        </el-col>
        <el-col :lg="8" :md="12" class="right">
            <h2 class="title">淘宝商城</h2>
            <div>
                <span class="line"></span>
                <span>基于 VUE3 + Vite 的超强商城</span>
                <span class="line"></span>
            </div>
            <div>
                <el-form ref="formRef" :model="form" class="w-[250px]" :rules="rules">
                    <el-form-item prop="username">
                        <el-input v-model="form.username" placeholder="请输入用户名">
                            <template #prefix>
                                <el-icon>
                                    <user />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item prop="password">
                        <el-input v-model="form.password" placeholder="请输入密码" type="password" show-password>
                            <template #prefix>
                                <el-icon>
                                    <lock />
                                </el-icon>
                            </template>
                        </el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button round color="#626aef" class="w-[250px]" type="primary" @click="onSubmit"
                            :loading="loading">登 录</el-button>
                    </el-form-item>
                </el-form>
            </div>
        </el-col>
    </el-row>
</template>

<script lang="ts" setup>
import { reactive, ref, onMounted, onBeforeUnmount } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router';
import { toast } from '~/composables/util'

const store = useStore()
const router = useRouter()
const loading = ref(false)

const form = reactive({
    username: 'admin',
    password: 'admin',
})

const rules = reactive({
    username: [
        { required: true, message: '用户名不能为空', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '密码不能为空', trigger: 'blur' }
    ]
})


const onSubmit = () => {
    loading.value = true
    store.dispatch("login", form).then(res => {
        toast("登录成功")
        router.push("/")
    }).finally(() => {
        loading.value = false
    })
}


// 添加键盘监听
onMounted(() => {
    document.addEventListener("keyup", onkeyup)
})
// 移除键盘监听
onBeforeUnmount(() => {
    document.removeEventListener("keyup", onkeyup)
})

// 监听回车事件
function onkeyup(e) {
    if (e.key == "Enter") {
        onSubmit()
    }
}

</script>

<style lang="postcss" scoped> .login-container {
     @apply min-h-screen bg-indigo-500;
 }

 .login-container .left,
 .login-container .right {
     @apply flex items-center justify-center;
 }

 .login-container .right {
     @apply bg-light-50 flex-col;
 }

 .left>div>div:first-child {
     @apply font-bold text-5xl text-light-50 mb-4;
 }

 .left>div>div:last-child {
     @apply text-gray-200 text-sm;
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