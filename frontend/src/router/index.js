import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import SignupUser from '../components/UserSignup.vue'
import UserLogin from '@/components/UserLogin.vue' 
import CategoryManage from '@/components/CategoryManage.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/signup',
    name: 'signup',
    component: SignupUser
  },
  {
    path: '/login',
    name: 'login',
    component: UserLogin
  },
  {
    path: '/categories',
    name: 'categories',
    component: CategoryManage,
    meta: { isAdmin: true }
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user_info'));

  if (to.meta.isAdmin && (user.role !== 'admin')) {
    next({path:'/login', query:{unauthorized:true}});
  } else {
    next();
  }
});


export default router
