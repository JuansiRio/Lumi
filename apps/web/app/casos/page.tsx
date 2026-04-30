"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useSession } from "next-auth/react";
import {
  useCallback,
  useEffect,
  useState,
  type ChangeEvent,
  type MouseEvent,
} from "react";

import type { Caso, TipoAccion } from "@/lib/api-client";

const API_BASE_URL: string =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

const TIPOS_ACCION: ReadonlyArray<{ value: TipoAccion; label: string }> = [
  { value: "ejecutivo", label: "Ejecutivo" },
  { value: "tutela", label: "Tutela" },
  { value: "laboral", label: "Laboral" },
  {
    value: "nulidad_restablecimiento",
    label: "Nulidad y restablecimiento del derecho",
  },
  { value: "reparacion_directa", label: "Reparación directa" },
  { value: "otro", label: "Otro" },
] as const;

type SessionUserWithId = {
  id?: string | null;
};

function readSessionUserId(sessionUser: unknown): string | undefined {
  if (sessionUser === null || sessionUser === undefined || typeof sessionUser !== "object") {
    return undefined;
  }
  const raw: unknown = (sessionUser as SessionUserWithId).id;
  if (typeof raw !== "string") {
    return undefined;
  }
  const trimmed: string = raw.trim();
  return trimmed.length > 0 ? trimmed : undefined;
}

async function parseJsonOrThrow(res: Response): Promise<unknown> {
  const text: string = await res.text();
  let body: unknown = null;
  if (text.length > 0) {
    try {
      body = JSON.parse(text) as unknown;
    } catch {
      body = { detail: text };
    }
  }
  if (!res.ok) {
    const detail: string =
      typeof body === "object" &&
      body !== null &&
      "detail" in body &&
      typeof (body as { detail: unknown }).detail === "string"
        ? (body as { detail: string }).detail
        : `Error HTTP ${String(res.status)}`;
    throw new Error(detail);
  }
  return body;
}

async function fetchCasosList(xUserId: string): Promise<Caso[]> {
  const headers: Headers = new Headers();
  headers.set("X-User-ID", xUserId);
  const res: Response = await fetch(`${API_BASE_URL}/casos/`, {
    method: "GET",
    headers,
    cache: "no-store",
  });
  const body: unknown = await parseJsonOrThrow(res);
  return body as Caso[];
}

async function fetchCrearCaso(
  xUserId: string,
  payload: { nombre_caso: string; tipo_accion: TipoAccion },
): Promise<Caso> {
  const headers: Headers = new Headers();
  headers.set("X-User-ID", xUserId);
  headers.set("Content-Type", "application/json");
  const res: Response = await fetch(`${API_BASE_URL}/casos/`, {
    method: "POST",
    headers,
    body: JSON.stringify(payload),
  });
  const body: unknown = await parseJsonOrThrow(res);
  return body as Caso;
}

export default function CasosPage(): JSX.Element {
  const router = useRouter();
  const { data: session, status } = useSession();
  const xUserId: string | undefined = readSessionUserId(session?.user);

  const [casos, setCasos] = useState<Caso[]>([]);
  const [cargando, setCargando] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [modalAbierto, setModalAbierto] = useState<boolean>(false);
  const [nombreCaso, setNombreCaso] = useState<string>("");
  const [tipoAccion, setTipoAccion] = useState<TipoAccion>("ejecutivo");
  const [creando, setCreando] = useState<boolean>(false);

  const cargarCasos = useCallback(async (): Promise<void> => {
    if (!xUserId) {
      setCasos([]);
      setCargando(false);
      return;
    }
    setCargando(true);
    setError(null);
    try {
      const data: Caso[] = await fetchCasosList(xUserId);
      setCasos(data);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "No se pudieron cargar los casos.");
    } finally {
      setCargando(false);
    }
  }, [xUserId]);

  useEffect(() => {
    if (status === "loading") {
      return;
    }
    if (status === "unauthenticated" || !xUserId) {
      setCasos([]);
      setCargando(false);
      return;
    }
    void cargarCasos();
  }, [status, xUserId, cargarCasos]);

  const onNombreChange = (e: ChangeEvent<HTMLInputElement>): void => {
    setNombreCaso(e.target.value);
  };

  const onTipoChange = (e: ChangeEvent<HTMLSelectElement>): void => {
    setTipoAccion(e.target.value as TipoAccion);
  };

  const cerrarModal = (): void => {
    setModalAbierto(false);
  };

  const abrirModal = (): void => {
    setModalAbierto(true);
  };

  const onBackdropClick = (e: MouseEvent<HTMLDivElement>): void => {
    if (e.target === e.currentTarget) {
      cerrarModal();
    }
  };

  const crearCaso = async (): Promise<void> => {
    const nombre: string = nombreCaso.trim();
    if (!nombre || creando || !xUserId) {
      return;
    }
    setCreando(true);
    setError(null);
    try {
      const c: Caso = await fetchCrearCaso(xUserId, {
        nombre_caso: nombre,
        tipo_accion: tipoAccion,
      });
      setModalAbierto(false);
      setNombreCaso("");
      setTipoAccion("ejecutivo");
      router.push(`/casos/${c.id}/chat`);
    } catch (e: unknown) {
      setError(e instanceof Error ? e.message : "No se pudo crear el caso.");
    } finally {
      setCreando(false);
    }
  };

  if (status === "loading") {
    return (
      <main className="min-h-screen bg-neutral-50 p-6 sm:p-8">
        <div className="mx-auto max-w-3xl">
          <p className="text-sm text-neutral-500">Cargando sesión…</p>
        </div>
      </main>
    );
  }

  if (status === "unauthenticated") {
    return (
      <main className="min-h-screen bg-neutral-50 p-6 sm:p-8">
        <div className="mx-auto max-w-3xl">
          <h1 className="text-2xl font-semibold text-primary">Casos</h1>
          <p className="mt-4 text-sm text-neutral-600">
            Inicie sesión para ver sus casos.{" "}
            <Link href="/login" className="font-medium text-primary underline">
              Ir a iniciar sesión
            </Link>
          </p>
        </div>
      </main>
    );
  }

  if (!xUserId) {
    return (
      <main className="min-h-screen bg-neutral-50 p-6 sm:p-8">
        <div className="mx-auto max-w-3xl">
          <h1 className="text-2xl font-semibold text-primary">Casos</h1>
          <p className="mt-4 text-sm text-red-800" role="alert">
            No se pudo obtener el identificador de usuario de la sesión. Vuelva a iniciar sesión.
          </p>
          <Link href="/login" className="mt-2 inline-block text-sm font-medium text-primary underline">
            Ir a iniciar sesión
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-neutral-50 p-6 sm:p-8">
      <div className="mx-auto max-w-3xl">
        <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
          <h1 className="text-2xl font-semibold text-primary">Casos</h1>
          <button
            type="button"
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white shadow hover:opacity-90"
            onClick={abrirModal}
          >
            Nuevo caso
          </button>
        </div>

        {error !== null && (
          <p className="mb-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-800" role="alert">
            {error}
          </p>
        )}

        {cargando && <p className="text-sm text-neutral-500">Cargando casos…</p>}

        {!cargando && casos.length === 0 && (
          <p className="text-sm text-neutral-600">
            No hay casos todavía. Cree uno con el botón «Nuevo caso».
          </p>
        )}

        <ul className="space-y-2">
          {casos.map((c: Caso) => (
            <li key={c.id}>
              <Link
                href={`/casos/${c.id}/chat`}
                className="block rounded-lg border border-neutral-200 bg-white p-4 shadow-sm transition hover:border-primary"
              >
                <span className="font-medium text-neutral-900">{c.nombre_caso}</span>
                <span className="mt-1 block text-xs text-neutral-600">
                  <span className="text-neutral-500">Tipo:</span> {c.tipo_accion}
                  <span className="mx-2 text-neutral-300">·</span>
                  <span className="text-neutral-500">Fase:</span> {c.fase_actual}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </div>

      {modalAbierto && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-nuevo-caso-titulo"
          onClick={onBackdropClick}
        >
          <div
            className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl"
            onClick={(e: MouseEvent<HTMLDivElement>) => {
              e.stopPropagation();
            }}
          >
            <h2 id="modal-nuevo-caso-titulo" className="text-lg font-semibold text-primary">
              Nuevo caso
            </h2>
            <label className="mt-4 block text-sm font-medium text-neutral-700" htmlFor="nc-nombre">
              Nombre del caso
            </label>
            <input
              id="nc-nombre"
              className="mt-1 w-full rounded-lg border border-neutral-300 px-3 py-2 text-sm text-neutral-900 outline-none focus:border-primary focus:ring-1 focus:ring-primary"
              value={nombreCaso}
              onChange={onNombreChange}
              autoFocus
            />
            <label className="mt-3 block text-sm font-medium text-neutral-700" htmlFor="nc-tipo">
              Tipo de acción
            </label>
            <select
              id="nc-tipo"
              className="mt-1 w-full rounded-lg border border-neutral-300 px-3 py-2 text-sm text-neutral-900 outline-none focus:border-primary focus:ring-1 focus:ring-primary"
              value={tipoAccion}
              onChange={onTipoChange}
            >
              {TIPOS_ACCION.map((t: { value: TipoAccion; label: string }) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
            <div className="mt-6 flex justify-end gap-2">
              <button
                type="button"
                className="rounded-lg px-3 py-2 text-sm text-neutral-600 hover:bg-neutral-100"
                onClick={cerrarModal}
              >
                Cancelar
              </button>
              <button
                type="button"
                className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
                disabled={creando || nombreCaso.trim().length === 0}
                onClick={() => void crearCaso()}
              >
                {creando ? "Creando…" : "Crear"}
              </button>
            </div>
          </div>
        </div>
      )}
    </main>
  );
}
