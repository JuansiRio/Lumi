"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import type { Caso, TipoAccion } from "@/lib/api-client";
import { createCaso, listCasos } from "@/lib/api-client";

const TIPOS: { value: TipoAccion; label: string }[] = [
  { value: "ejecutivo", label: "Ejecutivo" },
  { value: "tutela", label: "Tutela" },
  { value: "laboral", label: "Laboral" },
  { value: "nulidad_restablecimiento", label: "Nulidad y restablecimiento" },
  { value: "reparacion_directa", label: "Reparación directa" },
  { value: "otro", label: "Otro" },
];

export default function CasosPage() {
  const router = useRouter();
  const [casos, setCasos] = useState<Caso[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modal, setModal] = useState(false);
  const [nombre, setNombre] = useState("");
  const [tipo, setTipo] = useState<TipoAccion>("ejecutivo");
  const [creando, setCreando] = useState(false);

  const cargar = useCallback(async () => {
    setCargando(true);
    setError(null);
    try {
      const data = await listCasos();
      setCasos(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudieron cargar los casos.");
    } finally {
      setCargando(false);
    }
  }, []);

  useEffect(() => {
    void cargar();
  }, [cargar]);

  const crear = async () => {
    const n = nombre.trim();
    if (!n || creando) {
      return;
    }
    setCreando(true);
    setError(null);
    try {
      const c = await createCaso({ nombre_caso: n, tipo_accion: tipo });
      setModal(false);
      setNombre("");
      router.push(`/casos/${c.id}/chat`);
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo crear el caso.");
    } finally {
      setCreando(false);
    }
  };

  return (
    <main className="min-h-screen bg-neutral-50 p-6 sm:p-8">
      <div className="mx-auto max-w-3xl">
        <div className="mb-6 flex flex-wrap items-center justify-between gap-3">
          <h1 className="text-2xl font-semibold text-primary">Casos</h1>
          <button
            type="button"
            className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white shadow hover:opacity-90"
            onClick={() => setModal(true)}
          >
            Nuevo caso
          </button>
        </div>

        {error && (
          <p className="mb-4 rounded-md bg-red-50 px-3 py-2 text-sm text-red-800" role="alert">
            {error}
          </p>
        )}

        {cargando && <p className="text-sm text-neutral-500">Cargando…</p>}

        {!cargando && casos.length === 0 && (
          <p className="text-sm text-neutral-600">No hay casos todavía. Cree uno con el botón superior.</p>
        )}

        <ul className="space-y-2">
          {casos.map((c) => (
            <li key={c.id}>
              <Link
                href={`/casos/${c.id}/chat`}
                className="block rounded-lg border border-neutral-200 bg-white p-4 shadow-sm transition hover:border-primary"
              >
                <span className="font-medium text-neutral-900">{c.nombre_caso}</span>
                <span className="mt-1 block text-xs text-neutral-500">
                  {c.tipo_accion} · fase {c.fase_actual} · {c.estado}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </div>

      {modal && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4"
          role="dialog"
          aria-modal="true"
          aria-labelledby="modal-nuevo-caso"
        >
          <div className="w-full max-w-md rounded-xl bg-white p-6 shadow-xl">
            <h2 id="modal-nuevo-caso" className="text-lg font-semibold text-primary">
              Nuevo caso
            </h2>
            <label className="mt-4 block text-sm font-medium text-neutral-700" htmlFor="nc-nombre">
              Nombre del caso
            </label>
            <input
              id="nc-nombre"
              className="mt-1 w-full rounded-lg border border-neutral-300 px-3 py-2 text-sm outline-none ring-primary focus:border-primary focus:ring-1"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              autoFocus
            />
            <label className="mt-3 block text-sm font-medium text-neutral-700" htmlFor="nc-tipo">
              Tipo de acción
            </label>
            <select
              id="nc-tipo"
              className="mt-1 w-full rounded-lg border border-neutral-300 px-3 py-2 text-sm outline-none focus:border-primary focus:ring-1"
              value={tipo}
              onChange={(e) => setTipo(e.target.value as TipoAccion)}
            >
              {TIPOS.map((t) => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
            <div className="mt-6 flex justify-end gap-2">
              <button
                type="button"
                className="rounded-lg px-3 py-2 text-sm text-neutral-600 hover:bg-neutral-100"
                onClick={() => setModal(false)}
              >
                Cancelar
              </button>
              <button
                type="button"
                className="rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white disabled:opacity-50"
                disabled={creando || !nombre.trim()}
                onClick={() => void crear()}
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
