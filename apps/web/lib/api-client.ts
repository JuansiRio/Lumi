/**
 * Cliente HTTP hacia el backend FastAPI (proxy /api/casos en tareas posteriores).
 * Sin lógica de negocio en S0.2.
 */
export const API_BASE_URL: string =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";
