<template>
    <div class="f-header">
        <span class="logo">
            <el-icon class=" mr-1">
                <School />
            </el-icon>
            淘宝商城
        </span>
        <el-tooltip effect="dark" content="折叠" placement="bottom">
            <el-icon class="icon-btn" @click="$store.commit('handleAsideWidth')">
                <Fold v-if="$store.state.asideWidth == '250px'"/>
                <Expand v-else />
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
import { useFullscreen } from '@vueuse/core'
import FormDrawer from '~/components/FormDrawer.vue';
import { useRePassword, useLogout } from '~/composables/user'


const { handleLogout } = useLogout();
const { isFullscreen, toggle } = useFullscreen();
const {
        formDrawerRef,
        form,
        rules,
        onSubmit,
        openRePasswordForm
    } = useRePassword()
 

const handleRefresh = () => location.reload()

const handleCommand = (c) => {
    switch (c) {
        case "rePassword":
            openRePasswordForm()
            break
        case "logout":
            handleLogout()
            break
    }

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
