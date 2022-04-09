// import { createApp } from 'vue'
// import the root component App from a single-file component.
//import App from './App.vue'

const routes = [
    {path: '/basic', component:basic},
    {path: '/advanced', component:advanced}
]

const router = new VueRouter({
    //history: VueRouter.createWebHashHistory(), 
    routes
})

const app = new Vue({
    router
}).$mount('#app')