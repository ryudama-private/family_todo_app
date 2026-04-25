import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../pages/LoginPage.vue";
import FamilyRegisterPage from "../pages/FamilyRegisterPage.vue";
import TodoPage from "../pages/TodoPage.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "login", component: LoginPage },
  { path: "/todo", name: "todo", component: TodoPage },
  {
    path: "/family/register",
    name: "family-register",
    component: FamilyRegisterPage,
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

export default router;
