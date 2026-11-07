import type { Project, ProjectInput } from "../types";
import { request } from "./client";

export const getProjects = () => request<Project[]>("/projects");
export const getProject = (id: number) => request<Project>(`/projects/${id}`);
export const createProject = (data: ProjectInput) =>
  request<Project>("/projects", { method: "POST", body: data });
export const updateProject = (id: number, data: ProjectInput) =>
  request<Project>(`/projects/${id}`, { method: "PUT", body: data });