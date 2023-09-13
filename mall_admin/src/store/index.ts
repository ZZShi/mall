import { createStore } from 'vuex'
import { login, logout, getInfo } from '~/api/manage'
import { removeToken, setToken } from '~/composables/auth'
// 创建一个新的 store 实例
const store = createStore({
    state() {
        return {
            // 用户信息
            user: {}
        }
    },
    mutations: {
        // 记录用户信息
        SET_USERINFO(state: string, user: object) {
            state.user = user
        }
    },
    actions: {
        // 登录
        login({ commit }, { username, password }) {
            return new Promise((resolve, reject) => {
                login(username, password).then(res => {
                    setToken(res.token)
                    resolve(res)
                }).catch(err => reject(err))

            })
        },
        // 获取当前登录用户信息
        getInfo({ commit }) {
            return new Promise((resolve, reject) => {
                getInfo().then(res => {
                    commit("SET_USERINFO", res)
                    resolve(res)
                }).catch(err => reject(err))
            })
        },
        //  退出登录
        logout({ commit }) {
            return new Promise((resolve, reject) => {
                logout().then(res => {
                    // 移除 cookie
                    removeToken()
                    // 清除当前用户状态
                    commit("SET_USERINFO", {})
                    resolve(res)
                }).catch(err => reject(err))
            })
        },
    }
})


export default store;
