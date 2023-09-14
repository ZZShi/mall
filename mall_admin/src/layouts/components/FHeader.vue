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
    <el-drawer v-model="drawer" title="修改密码" size="45%">
        <span>Hi there!</span>
    </el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import store from '~/store';
import { showModal, toast } from '~/composables/util';
import { useRouter } from 'vue-router';
import { useFullscreen } from '@vueuse/core'

const { isFullscreen, toggle } = useFullscreen()

const router = useRouter()

const drawer = ref(false)

const handleRefresh = () => location.reload()

const handleCommand = (c) => {
    switch (c) {
        case "rePassword":
            console.log("Todo 修改密码")
            drawer.value = true
            break
        case "logout":
            handleLogout()
            break
    }

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

<style lang="postcss" scoped>
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
