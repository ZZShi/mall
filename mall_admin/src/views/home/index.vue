<template>
    <div>Home</div>
    <el-button @click="set">设置</el-button>
    <el-button @click="get">获取</el-button>
    <el-button @click="remove">移除</el-button>
    {{ $store.state.user }}
</template>

<script lang="ts" setup>
import { useCookies } from '@vueuse/integrations/useCookies'

const cookies = useCookies()
console.log(cookies)

function set() {
    cookies.set("admin-token", "123456")
}

function get() {
    console.log(cookies.get("admin-token")) 
}

function remove() {
    cookies.remove("admin-token")
}

</script>