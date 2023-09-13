import store from "~/store"
import router from "~/router"

import { toast } from "~/composables/util"
import { getToken } from "~/composables/auth"


// 全局前置守卫
router.beforeEach(async (to, from, next) => {

    const token = getToken()

    // 没有登录，强制跳转到登录页
    if(!token && to.path != "/login"){
        toast("请先登录", "warning")
        return next({
            path: "/login"
        })
    }

    // 防止重复登录
    if(token && to.path == "/login"){
        toast("请勿重复登录", "warning")
        return next({
            path: from.path ? from.path : "/"
        })
    }

    // 如果用户登录了，自动获取用户信息，并存储在 vuex 中
    if(token){
        await store.dispatch("getInfo")
    }

    // 放行
    next()
})