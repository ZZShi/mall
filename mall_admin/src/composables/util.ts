import { ElNotification, ElMessageBox } from 'element-plus'
import nprogress from 'nprogress'


export function toast(message: string, type: string = "success") {
    ElNotification({
        message,
        type,
        duration: 500
      })
}


export function showModal(content: string = "提示内容", type: string = "warning", title: string = "") {
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

// 显示全屏 loading
export function showFullLoading() {
  nprogress.start();
}


// 隐藏全屏 loading
export function hideFullLoading() {
  nprogress.done();
}
