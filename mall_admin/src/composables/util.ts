import { ElNotification } from 'element-plus'


export function toast(message: string, type: string = "success") {
    ElNotification({
        message,
        type,
        duration: 3000
      })
}
