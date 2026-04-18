/**
 * Cliente HTTP tipado hacia el backend FastAPI (Brief 3.4).
 */

export const API_BASE_URL: string =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

const X_USER_STORAGE_KEY = "lumi_x_user_id";

export function getXUserId(): string {
  if (typeof window === "undefined") {
    return process.env.NEXT_PUBLIC_X_USER_ID ?? "";
  }
  const fromEnv = process.env.NEXT_PUBLIC_X_USER_ID?.trim();
  if (fromEnv) {
    return fromEnv;
  }
  let id = window.sessionStorage.getItem(X_USER_STORAGE_KEY);
  if (!id) {
    id = crypto.randomUUID();
    window.sessionStorage.setItem(X_USER_STORAGE_KEY, id);
  }
  return id;
}

function headersBase(): Headers {
  const h = new Headers();
  h.set("X-User-ID", getXUserId());
  return h;
}

async function parseJsonOrError(res: Response): Promise<unknown> {
  const text = await res.text();
  let body: unknown = null;
  if (text) {
    try {
      body = JSON.parse(text) as unknown;
    } catch {
      body = { detail: text };
    }
  }
  if (!res.ok) {
    const detail =
      typeof body === "object" &&
      body !== null &&
      "detail" in body &&
      typeof (body as { detail: unknown }).detail === "string"
        ? (body as { detail: string }).detail
        : `Error HTTP ${res.status}`;
    throw new Error(detail);
  }
  return body;
}

export type TipoAccion =
  | "ejecutivo"
  | "tutela"
  | "laboral"
  | "nulidad_restablecimiento"
  | "reparacion_directa"
  | "otro";

export type EstadoCaso = "activo" | "pausado" | "cerrado";

export type EstadoDocumento = "pendiente" | "procesando" | "listo" | "error";

export interface Caso {
  id: string;
  nombre_caso: string;
  tipo_accion: TipoAccion;
  estado: EstadoCaso;
  fase_actual: string;
  tokens_consumidos: number;
  costo_usd: number;
  created_at: string;
  updated_at: string;
}

export interface CasoCreateBody {
  nombre_caso: string;
  tipo_accion: TipoAccion;
}

export interface CasoPatchBody {
  estado?: EstadoCaso;
  fase_actual?: string;
}

export interface MensajeHistorial {
  id: string | null;
  rol: string;
  contenido: string;
  fase: string | null;
  created_at: string | null;
}

export interface LumiCoreResponse {
  respuesta: string;
  fase_output: Record<string, unknown> | null;
  subagente_llamado: string | null;
  tokens_usados: number;
  costo_usd: number;
}

export interface Documento {
  id: string;
  caso_id: string;
  nombre_original: string;
  mime_type: string;
  tipo_detectado: string | null;
  estado: EstadoDocumento;
  texto_extraido: string | null;
  storage_path: string | null;
  created_at: string;
  updated_at: string;
}

export interface DocumentoUploadResponse {
  documento: Documento;
  tokens_usados: number;
  costo_usd: number;
}

export interface FaseOutput {
  caso_id: string;
  fase: string;
  version: number;
  contenido: Record<string, unknown>;
  aprobado_abogado: boolean;
  anotaciones: string | null;
  tokens_usados: number;
  costo_usd: number;
}

export interface AprobarFaseResponse {
  fase_aprobada: string;
  nueva_fase_actual: string;
  tokens_resumen: number;
  costo_resumen_usd: number;
}

export interface CostosResumen {
  tokens_input_trazabilidad: number;
  tokens_output_trazabilidad: number;
  tokens_total_trazabilidad: number;
  costo_usd_trazabilidad: number;
  tokens_consumidos_caso: number;
  costo_usd_caso: number;
}

export async function listCasos(): Promise<Caso[]> {
  const res = await fetch(`${API_BASE_URL}/casos/`, {
    method: "GET",
    headers: headersBase(),
  });
  const body = await parseJsonOrError(res);
  return body as Caso[];
}

export async function createCaso(body: CasoCreateBody): Promise<Caso> {
  const h = headersBase();
  h.set("Content-Type", "application/json");
  const res = await fetch(`${API_BASE_URL}/casos/`, {
    method: "POST",
    headers: h,
    body: JSON.stringify(body),
  });
  const out = await parseJsonOrError(res);
  return out as Caso;
}

export async function getCaso(casoId: string): Promise<Caso> {
  const res = await fetch(`${API_BASE_URL}/casos/${encodeURIComponent(casoId)}`, {
    method: "GET",
    headers: headersBase(),
  });
  const body = await parseJsonOrError(res);
  return body as Caso;
}

export async function patchCaso(casoId: string, body: CasoPatchBody): Promise<Caso> {
  const h = headersBase();
  h.set("Content-Type", "application/json");
  const res = await fetch(`${API_BASE_URL}/casos/${encodeURIComponent(casoId)}`, {
    method: "PATCH",
    headers: h,
    body: JSON.stringify(body),
  });
  const out = await parseJsonOrError(res);
  return out as Caso;
}

export async function postChat(casoId: string, mensaje: string): Promise<LumiCoreResponse> {
  const h = headersBase();
  h.set("Content-Type", "application/json");
  const res = await fetch(`${API_BASE_URL}/casos/${encodeURIComponent(casoId)}/chat`, {
    method: "POST",
    headers: h,
    body: JSON.stringify({ mensaje }),
  });
  const body = await parseJsonOrError(res);
  return body as LumiCoreResponse;
}

export async function getChatHistorial(casoId: string, n: number = 50): Promise<MensajeHistorial[]> {
  const q = new URLSearchParams({ n: String(n) });
  const res = await fetch(
    `${API_BASE_URL}/casos/${encodeURIComponent(casoId)}/chat/historial?${q.toString()}`,
    { method: "GET", headers: headersBase() },
  );
  const body = await parseJsonOrError(res);
  return body as MensajeHistorial[];
}

export async function listDocumentos(casoId: string): Promise<Documento[]> {
  const res = await fetch(`${API_BASE_URL}/casos/${encodeURIComponent(casoId)}/documentos`, {
    method: "GET",
    headers: headersBase(),
  });
  const body = await parseJsonOrError(res);
  return body as Documento[];
}

export async function postDocumento(casoId: string, file: File): Promise<DocumentoUploadResponse> {
  const fd = new FormData();
  fd.append("file", file);
  const h = headersBase();
  const res = await fetch(`${API_BASE_URL}/casos/${encodeURIComponent(casoId)}/documentos`, {
    method: "POST",
    headers: h,
    body: fd,
  });
  const body = await parseJsonOrError(res);
  return body as DocumentoUploadResponse;
}

export async function listFaseOutputs(casoId: string): Promise<FaseOutput[]> {
  const res = await fetch(`${API_BASE_URL}/casos/${encodeURIComponent(casoId)}/fases`, {
    method: "GET",
    headers: headersBase(),
  });
  const body = await parseJsonOrError(res);
  return body as FaseOutput[];
}

export async function aprobarFase(casoId: string, fase: string): Promise<AprobarFaseResponse> {
  const res = await fetch(
    `${API_BASE_URL}/casos/${encodeURIComponent(casoId)}/fases/${encodeURIComponent(fase)}/aprobar`,
    { method: "POST", headers: headersBase() },
  );
  const body = await parseJsonOrError(res);
  return body as AprobarFaseResponse;
}

export function getBorradorDownloadUrl(casoId: string): string {
  return `${API_BASE_URL}/casos/${encodeURIComponent(casoId)}/borrador`;
}

export async function downloadBorrador(casoId: string, nombreArchivo?: string): Promise<void> {
  const res = await fetch(getBorradorDownloadUrl(casoId), {
    method: "GET",
    headers: headersBase(),
  });
  if (!res.ok) {
    const text = await res.text();
    let detail = `Error HTTP ${res.status}`;
    try {
      const j = JSON.parse(text) as { detail?: string };
      if (typeof j.detail === "string") {
        detail = j.detail;
      }
    } catch {
      if (text) {
        detail = text;
      }
    }
    throw new Error(detail);
  }
  const blob = await res.blob();
  const dispo = res.headers.get("Content-Disposition");
  let filename = nombreArchivo ?? "borrador.docx";
  if (dispo) {
    const m = /filename="?([^";]+)"?/i.exec(dispo);
    if (m?.[1]) {
      filename = m[1];
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

export async function getCostos(casoId: string): Promise<CostosResumen> {
  const res = await fetch(`${API_BASE_URL}/casos/${encodeURIComponent(casoId)}/costos`, {
    method: "GET",
    headers: headersBase(),
  });
  const body = await parseJsonOrError(res);
  return body as CostosResumen;
}
