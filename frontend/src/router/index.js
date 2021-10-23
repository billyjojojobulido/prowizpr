import Vue from 'vue'
import Router from 'vue-router'
// import store from '../store'

Vue.use(Router)
import Forum from "@/components/forum/Forum";
import Goal from "@/components/goal/Goal";
import LogIn from "@/components/LogIn";
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
        }
    ]
})

// router.beforeEach((to, from, next) => {
//     if (!store.state.authenticated && to.name !== 'Login') {
//         next('/')
//     } else {
//         next()
//     }
// })

export default router
