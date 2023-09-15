<template>
    <div class="f-header">
        <span class="logo">
            <el-icon class=" mr-1">
                <School />
            </el-icon>
            淘宝商城
        </span>
        <el-tooltip effect="dark" content="折叠" placement="bottom">
            <el-icon class="icon-btn">
                <Fold />
            </el-icon>
        </el-tooltip>
        <el-tooltip effect="dark" content="刷新" placement="bottom">
            <el-icon @click="handleRefresh" class="icon-btn">
                <Refresh />
            </el-icon>
        </el-tooltip>

        <div class=" ml-auto flex items-center">
            <el-tooltip effect="dark" content="切换全屏" placement="bottom">
                <el-icon @click="toggle" class="icon-btn">
                    <FullScreen v-if="!isFullscreen" />
                    <Aim v-else />
                </el-icon>
            </el-tooltip>
            <el-dropdown class="dropdown" @command="handleCommand">
                <span class=" flex items-center text-light-50">
                    <el-avatar class="mr-2" :size="25" :src="$store.state.user.avatar" />
                    {{ $store.state.user.username }}
                    <el-icon class="el-icon--right">
                        <arrow-down />
                    </el-icon>
                </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item command="rePassword">修改密码</el-dropdown-item>
                        <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                    </el-dropdown-menu>

                </template>
            </el-dropdown>
        </div>
    </div>
    <form-drawer ref="formDrawerRef" title="修改密码" destoryOnClose @submit="onSubmit">
        <el-form ref="formRef" :rules="rules" :model="form" label-width="80px" size="small">
            <el-form-item prop="oldpassword" label="旧密码">
                <el-input v-model="form.oldpassword" placeholder="请输入旧密码">
                </el-input>
            </el-form-item>
            <el-form-item prop="password" label="新密码">
                <el-input v-model="form.password" placeholder="请输入新密码" type="password">
                </el-input>
            </el-form-item>
            <el-form-item prop="repassword" label="确认密码">
                <el-input v-model="form.repassword" placeholder="请输入确认密码" type="password">
                </el-input>
            </el-form-item>
        </el-form>
    </form-drawer>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import store from '~/store';
import { showModal, toast } from '~/composables/util';
import { useRouter } from 'vue-router';
import { useFullscreen } from '@vueuse/core'
import FormDrawer from '~/components/FormDrawer.vue';
import { updatePassword } from '~/api/manage';

const { isFullscreen, toggle } = useFullscreen()

const router = useRouter()
const form = ref({
    "oldpassword": "admin",
    "password": "12345",
    "repassword": "12345"
})

const rules = reactive({
    oldpassword: [
        { required: true, message: '旧密码不能为空', trigger: 'blur' }
    ],
    password: [
        { required: true, message: '新密码不能为空', trigger: 'blur' }
    ],
    repassword: [
        { required: true, message: '确认密码不能为空', trigger: 'blur' }
    ]
})

const formDrawerRef = ref(null)

const handleRefresh = () => location.reload()

const handleCommand = (c) => {
    switch (c) {
        case "rePassword":
            console.log("Todo 修改密码")
            formDrawerRef.value.open()
            break
        case "logout":
            handleLogout()
            break 
    }

}

function onSubmit() {
    formDrawerRef.value.showLoading()
    updatePassword(form.value).then(res=>{
        toast("修改密码成功")
        store.dispatch("logout")
        router.push("/login")
    }).finally(()=>{
        formDrawerRef.value.hideLoading()
    })

}

function handleLogout() {
    showModal("是否退出登录？").then(res => {
        console.log("确认退出登录")
        store.dispatch("logout").then(res => {
            // 提示退出登录成功
            toast("退出登录成功")
            // 跳转回登录页
            router.push("/login")
        })
    }).catch(err => {
        console.log("取消退出登录")
    })
}
</script>

<style lang="postcss">
.f-header {
    @apply flex items-center bg-indigo-700 text-light-50 fixed top-0 left-0 right-0;
    height: 60px;
}

.logo {
    @apply flex justify-center items-center text-xl font-thin;
    width: 250px;
}

.icon-btn {
    @apply flex justify-center items-center;
    width: 40px;
    height: 60px;
    cursor: pointer;
}

.icon-btn:hover {
    @apply bg-indigo-600
}

.dropdown {
    @apply flex justify-center items-center mx-5;
}
</style>
