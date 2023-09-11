<template>
    <div>
        <el-result title="404 Not Found" sub-title="Sorry, request error">
            <template #icon>
                <el-image
                    src="https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png" />
            </template>
            <template #extra>
                <el-button type="primary" @click="$router.push('/')">Go Home</el-button>
            </template>
        </el-result>
    </div>
</template>