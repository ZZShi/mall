<template>
    <div>Home</div>
    <el-button @click="handleLogout">退出登录</el-button>
</template>

<script lang="ts" setup>
import store from '~/store';
import { showModal, toast } from '~/composables/util';
import { useRouter } from 'vue-router';

const router = useRouter()


function handleLogout() {
    showModal("是否退出登录？").then(res=>{
        console.log("确认退出登录")
        store.dispatch("logout").then( res=>{
            // 提示退出登录成功
            toast("退出登录成功") 
            // 跳转回登录页
            router.push("/login")
        })
           
    }).catch(err=>{
        console.log("取消退出登录")
    })
}
</script>