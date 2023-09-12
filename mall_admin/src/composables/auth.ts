import { useCookies } from '@vueuse/integrations/useCookies'


const tokenKey = "admin-token"
const cookies = useCookies()

// 设置 token
export function setToken(token: string) {
    cookies.set(tokenKey, token)
}

// 获取 token
export function getToken(): string {
    return cookies.get("admin-token")
}

// 清除 token
export function removeToken() {
    cookies.remove(tokenKey)
}
