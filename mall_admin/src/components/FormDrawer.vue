<template>
  <el-drawer v-model="showDrawer" 
  :title="title" 
  :size="size" 
  :destoryOnClose="destoryOnClose"
  :close-on-click-modal="false">
    <div class="formDrawer">
        <div class="body">
            <slot></slot>
        </div>
        <div class="actions">
            <el-button type="primary" @click="submit" :loading="loading">{{ confirmText }}</el-button>
            <el-button type="default" @click="close">取消</el-button>
        </div>
    </div>
</el-drawer>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
const showDrawer = ref(false)
const loading = ref(false)
const showLoading = () => loading.value = true
const hideLoading = () => loading.value = false

const props = defineProps({
    title: String,
    size: {
        type: String,
        default: "45%"
    },
    destoryOnClose: {
        type: Boolean,
        default: false
    },
    confirmText: {
        type: String,
        default: "提交"
    },
})

// 提交
const emit = defineEmits(["submit"])
const submit = ()=> emit("submit")

// 打开
const open = () => showDrawer.value = true
// 关闭
const close = () => showDrawer.value = false
// 向父组件暴露以下方法
defineExpose({
    open,
    close,
    showLoading,
    hideLoading
})

</script>

<style lang="postcss">
.formDrawer {
    width: 100%;
    height: 100%;
    position: relative;
    @apply flex flex-col;
}
.formDrawer .body {
    flex: 1;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 50px;
    overflow-y: auto;
}
.formDrawer .actions {
    height: 50px;
    @apply mt-auto flex items-center;
}
</style>