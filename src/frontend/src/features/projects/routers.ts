
import type { RouteObject } from "react-router";
import AppLayout from "@/core/AppLayout";
import ProjectListPages from "./pages/ProjectListPage";

export const ProjectRoutes: RouteObject[] = [
  {
    path: "/projects",
    Component: AppLayout,
    children: [
      {
        path:"",
        Component: ProjectListPages
      }
    ]
  },
];
