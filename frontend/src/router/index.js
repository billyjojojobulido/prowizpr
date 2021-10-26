import Vue from 'vue'
import Router from 'vue-router'
import store from '../store'

Vue.use(Router)
import Forum from "@/components/forum/Forum";
import Goal from "@/components/goal/Goal";
import ForgetPassword from "@/components/profile/ForgetPassword";
import LogIn from "@/components/LogIn";
import Register from "@/components/profile/Register";
import Profile from "@/components/profile/Profile";
const router = new Router({
    routes: [
        {
            path: '/',
            name: 'Login',
            component: LogIn,
        },
        {
            path: '/forum',
            name: 'Forum',
            component: Forum,
        },
        {
            path: '/goal',
            name: 'Goal',
            component: Goal,
        },
        {
            path: '/forget_password',
            name: 'ForgetPassword',
            component: ForgetPassword,
        },
        {
            path: '/register',
            name: 'Register',
            component: Register,
        },
        {
            path: '/profile',
            name: 'Profile',
            component: Profile,
        }
    ]
})

router.beforeEach((to, from, next) => {
    if (!store.state.authenticated
        && to.name !== 'Login'
        && to.name !== 'ForgetPassword'
        && to.name !== 'Register'
    ) {
        next('/')
    } else {
        next()
    }
})

export default router
