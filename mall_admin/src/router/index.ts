import {
    createRouter,
    createWebHashHistory
} from 'vue-router'
import Index from '~/views/home/index.vue'
import About from '~/views/home/about.vue'
import Login from '~/views/home/login.vue'
import NotFound from '~/views/home/404.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            component: Index,
            meta: {
                "title": "首页"
            }
        },
        {
            path: "/about",
            component: About,
            meta: {
                "title": "关于页"
            }
        },
        {
            path: "/login",
            component: Login,
            meta: {
                "title": "登录页"
            }
        },
        { 
            path: '/:pathMatch(.*)*', 
            component: NotFound,
            meta: {
                "title": "404 页"
            }
        },
    ]
})

export default router;
