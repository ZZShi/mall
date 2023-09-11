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
            component: Index
        },
        {
            path: "/about",
            component: About
        },
        {
            path: "/login",
            component: Login
        },
        { 
            path: '/:pathMatch(.*)*', 
            component: NotFound 
        },
    ]
})

export default router
