import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../pages/LoginPage.vue";
import FamilyRegisterPage from "../pages/FamilyRegisterPage.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "login", component: LoginPage },
  {
    path: "/family/register",
    name: "family-register",
    component: FamilyRegisterPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
