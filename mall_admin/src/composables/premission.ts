import router from "~/router"
import { getToken } from "~/composables/auth"
import { toast } from "~/composables/util"


// 全局前置守卫
router.beforeEach((to, from, next) => {

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

    // 放行
    next()
})