import type { Task, TaskInput } from "../types";
import { request } from "./client";

export const getTasks = (projectId: number) =>
  request<Task[]>(`/tasks?project_id=${projectId}`);
export const createTask = (data: TaskInput) =>
  request<Task>("/tasks", { method: "POST", body: data });
export const updateTask = (id: number, data: TaskInput) =>
  request<Task>(`/tasks/${id}`, { method: "PUT", body: data });
export const deleteTask = (id: number) =>
  request<void>(`/tasks/${id}`, { method: "DELETE" });