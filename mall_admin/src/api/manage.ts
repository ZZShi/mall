import { service } from '~/axios'


export function login(username: string, password: string){
    return service.post("/admin/login", {
        username,
        password
    })
}