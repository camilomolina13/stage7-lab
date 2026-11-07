import { API_BASE_URL } from "../config";
import type { ApiErrorBody, FieldErrors } from "../types";

export class ApiError extends Error {
  status: number;
  code: string;
  details?: FieldErrors;

  constructor(status: number, code: string, message: string, details?: FieldErrors) {
    super(message);
    this.status = status;
    this.code = code;
    this.details = details;
  }
}

interface RequestOptions {
  method?: string;
  body?: unknown;
}

export async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const hasBody = options.body !== undefined;
  let response: Response;

  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      method: options.method ?? "GET",
      headers: hasBody ? { "Content-Type": "application/json" } : undefined,
      body: hasBody ? JSON.stringify(options.body) : undefined,
    });
  } catch {
    // fetch solo lanza error si no hay conexión con el servidor
    throw new ApiError(0, "network_error", "Could not connect to the server. Is the API running?");
  }

  if (response.status === 204) return undefined as T; // DELETE: sin body

  let data: unknown = null;
  try {
    data = await response.json();
  } catch {
    data = null;
  }

  if (!response.ok) {
    const err = (data as ApiErrorBody | null)?.error;
    throw new ApiError(
      response.status,
      err?.code ?? "unknown_error",
      err?.message ?? `Request failed (${response.status}).`,
      err?.details,
    );
  }
  return data as T;
}

/** Convierte cualquier error en un mensaje general + errores por campo. */
export function describeError(err: unknown): { message: string; fields: FieldErrors } {
  if (err instanceof ApiError) {
    const fields = { ...(err.details ?? {}) };
    const schema = fields._schema?.join(" ");
    delete fields._schema;
    if (schema) return { message: schema, fields };
    if (err.code === "validation_error") {
      return { message: "Please fix the errors below.", fields };
    }
    return { message: err.message, fields };
  }
  return { message: "Something went wrong. Please try again.", fields: {} };
}