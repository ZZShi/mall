import {
    createRouter,
    createWebHashHistory
} from 'vue-router'
import Admin from '~/layouts/admin.vue'
import Index from '~/views/home/index.vue'
import About from '~/views/home/about.vue'
import Login from '~/views/home/login.vue'
import NotFound from '~/views/home/404.vue'
import GoodsList from '~/views/goods/list.vue'

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            component: Admin,
            children: [
                {
                    path: "/",
                    component: Index,
                    meta: {
                        "title": "首页"
                    }
                },
                {
                    path: "/goods/list",
                    component: GoodsList,
                    meta: {
                        "title": "商品管理"
                    }
                }
            ]
            
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
