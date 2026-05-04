import { createRouter, createWebHistory } from "vue-router";
import LoginPage from "../pages/LoginPage.vue";
import FamilyRegisterPage from "../pages/FamilyRegisterPage.vue";
import TopPage from "../pages/TopPage.vue";
import TasksPage from "../pages/TasksPage.vue";
import CalendarPage from "../pages/CalendarPage.vue";

const routes = [
  { path: "/", redirect: "/login" },
  { path: "/login", name: "login", component: LoginPage },
  {
    path: "/todo",
    component: TopPage,
    children: [
      { path: "", redirect: "/todo/tasks" },
      { path: "tasks", name: "tasks", component: TasksPage },
      { path: "calendar", name: "calendar", component: CalendarPage },
    ],
  },
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
