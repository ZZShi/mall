import { ElNotification, ElMessageBox } from 'element-plus'


export function toast(message: string, type: string = "success") {
    ElNotification({
        message,
        type,
        duration: 3000
      })
}


export function showModal(content: string = "提示内容", type: string = "warning", title: string = ""){
  return ElMessageBox.confirm(
    content,
    title,
    {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type,
    }
  )
}
