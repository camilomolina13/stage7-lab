const raw = import.meta.env.VITE_API_BASE_URL as string | undefined;

// Única fuente de la URL. Se quitan las barras finales para evitar "//projects".
export const API_BASE_URL = (raw ?? "http://localhost:8000/api").replace(/\/+$/, "");