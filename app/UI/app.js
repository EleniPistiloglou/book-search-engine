const routes = [
    {
        path: '/recomendations',
        name: 'recomendations',
        component: recomendations,
      },
    {path: '/basic', component:basic},
    {path: '/advanced', component:advanced},
]

const router = new VueRouter({
    //history: VueRouter.createWebHashHistory(), 
    routes
})

const app = new Vue({
    router
}).$mount('#app')
