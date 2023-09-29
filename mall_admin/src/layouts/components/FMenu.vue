<template>
    <div class="f-menu" :style="{ width: $store.state.asideWidth }">
        <el-menu :default-active="defaultActive" class="border-0" @select="handleSelect" 
        unique-opened
        :collapse="isCollapse"
        :collapse-transition="false">
            <template v-for="(item, index) in asideMenu" :key="index">
                <el-sub-menu v-if="item.child && item.child.length > 0" :index="item.name">
                    <template #title>
                        <el-icon>
                            <component :is="item.icon"></component>
                        </el-icon>
                        <span>{{ item.name }}</span>
                    </template>
                    <el-menu-item v-for="(item2, index2) in item.child" :key="index2" :index="item2.frontpath">
                        <el-icon>
                            <component :is="item2.icon"></component>
                        </el-icon>
                        <span>{{ item2.name }}</span>
                    </el-menu-item>
                </el-sub-menu>
                <el-menu-item v-else :index="item.frontpath">
                    <el-icon>
                        <component :is="item.icon"></component>
                    </el-icon>
                    <span>{{ item.name }}</span>
                </el-menu-item>
            </template>
        </el-menu>
    </div>
</template> 
  
<script lang="ts" setup>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router';

const store = useStore()
const route = useRoute()
const router = useRouter()

// 是否折叠
const isCollapse = computed(() => !(store.state.asideWidth == '250px'))

const defaultActive = ref(route.path)

const handleSelect = (e) => {
    router.push(e)
}  

const asideMenu = [{
    "name": "后台面板",
    "icon": "help",
    "child": [{
        "name": "主控台",
        "icon": "home-filled",
        "frontpath": "/"
    }]
}, {
    "name": "商城管理",
    "icon": "shopping-bag",
    "child": [{
        "name": "商品管理",
        "icon": "home-filled",
        "frontpath": "/goods/list"
    }]
}]
</script>
  
<style lang="postcss">
.f-menu {
    transition: all 0.1s;
    top: 64px;
    bottom: 0;
    left: 0;
    overflow-y: auto;
    overflow-x: hidden;
    @apply shadow-md fixed bg-light-50
}
</style>