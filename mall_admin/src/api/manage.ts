import { service } from '~/axios'

// 登录
export function login(username: string, password: string) {
    return service.post("/admin/login", {
        username,
        password
    })
}

// 获取用户信息
export function getInfo() {
    return service.post("/admin/getinfo")
}
