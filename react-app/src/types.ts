export const STATUSES = ["TODO", "IN_PROGRESS", "DONE"] as const;
export const PRIORITIES = ["LOW", "MEDIUM", "HIGH"] as const;

export type Status = (typeof STATUSES)[number];
export type Priority = (typeof PRIORITIES)[number];

export interface Project {
  id: number;
  name: string;
  description: string;
  created_at: string;
}
export type ProjectInput = Pick<Project, "name" | "description">;

export interface Task {
  id: number;
  project_id: number;
  title: string;
  description: string;
  status: Status;
  priority: Priority;
  due_date: string | null; // "YYYY-MM-DD"
  created_at: string;
  updated_at: string;
}
export type TaskInput = Omit<Task, "id" | "created_at" | "updated_at">;

// Errores por campo del contrato: { title: ["This field is required."] }
export type FieldErrors = Record<string, string[]>;

export interface ApiErrorBody {
  error: { code: string; message: string; details?: FieldErrors };
}