import { api } from "@lib/api";
import type { ProjectModel } from "../types/product.types";

export async function getProject(): Promise<ProjectModel[]> {
  const res = await api.get<ProjectModel[]>("/project");
  return res.data;
}
