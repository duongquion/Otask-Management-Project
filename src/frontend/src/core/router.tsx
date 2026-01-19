import { ProjectRoutes } from "@/features/projects/routers";
import { useRoutes } from "react-router-dom";

export const appRoutes = [...ProjectRoutes];

export const AppRouter = () => {
  const element = useRoutes(appRoutes);
  return element;
};