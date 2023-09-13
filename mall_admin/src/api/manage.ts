import axios from '~/axios'

// 登录
export function login(username: string, password: string) {
    return axios.post("/admin/login", {
        username,
        password
    })
}

// 退出登录
export function logout() {
    return axios.post("/admin/logout")
}

// 获取用户信息
export function getInfo() {
    return axios.post("/admin/getinfo")
}
