import { ref, reactive } from 'vue'
import store from '~/store';
import { useRouter } from 'vue-router';
import { toast, showModal } from '~/composables/util';
import { updatePassword } from '~/api/manage';


export function useRePassword() {
    const router = useRouter()
    const formDrawerRef = ref(null)

    const form = ref({
        "oldpassword": "admin",
        "password": "12345",
        "repassword": "12345"
    })

    const rules = reactive({
        oldpassword: [
            { required: true, message: '旧密码不能为空', trigger: 'blur' }
        ],
        password: [
            { required: true, message: '新密码不能为空', trigger: 'blur' }
        ],
        repassword: [
            { required: true, message: '确认密码不能为空', trigger: 'blur' }
        ]
    })

    const openRePasswordForm = () => formDrawerRef.value.open()

    function onSubmit() {
        formDrawerRef.value.showLoading()
        updatePassword(form.value).then(res => {
            toast("修改密码成功")
            store.dispatch("logout")
            router.push("/login")
        }).finally(() => {
            formDrawerRef.value.hideLoading()
        })
    }

    return {
        formDrawerRef,
        form,
        rules,
        onSubmit,
        openRePasswordForm
    }
}

export function useLogout() { 
    const router = useRouter()

    function handleLogout() {
        showModal("是否退出登录？").then(res => {
            store.dispatch("logout").then(res => {
                // 提示退出登录成功
                toast("退出登录成功")
                // 跳转回登录页
                router.push("/login")
            })
        }).catch(err => {
            console.log("取消退出登录")
        })
    }

    return {
        handleLogout,
    }
}
