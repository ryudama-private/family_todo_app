import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../pages/LoginPage.vue";
import FamilyAddPage from "../pages/FamilyAddPage.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "login", component: LoginPage },
  { path: "/family/add", name: "family-add", component: FamilyAddPage },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
