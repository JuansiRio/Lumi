"use client";

import { useState } from "react";

import { aprobarFase } from "@/lib/api-client";

const FASES_ORDEN: readonly { code: string; label: string }[] = [
  { code: "0E", label: "0E Ético" },
  { code: "0A", label: "0A Hechos" },
  { code: "0C", label: "0C Estrategia" },
  { code: "1A", label: "1A Cliente" },
  { code: "1C", label: "1C Teoría" },
  { code: "2A", label: "2A Prob." },
  { code: "5A", label: "5A Advers." },
  { code: "GEN", label: "GEN Doc." },
] as const;

type FaseIndicatorProps = {
  casoId: string;
  faseActual: string;
  onFaseChanged: () => void;
};

export function FaseIndicator({ casoId, faseActual, onFaseChanged }: FaseIndicatorProps) {
  const [procesando, setProcesando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fNorm = faseActual.trim().toUpperCase();
  const idxActual = FASES_ORDEN.findIndex((f) => f.code === fNorm);

  const aprobar = async () => {
    if (!casoId || !fNorm || procesando) {
      return;
    }
    setProcesando(true);
    setError(null);
    try {
      await aprobarFase(casoId, fNorm);
      onFaseChanged();
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo aprobar la fase.");
    } finally {
      setProcesando(false);
    }
  };

  return (
    <nav className="border-b border-neutral-200 bg-neutral-50 px-4 py-3" aria-label="Fases">
      {error && (
        <p className="mb-2 text-xs text-red-700" role="alert">
          {error}
        </p>
      )}
      <div className="flex flex-wrap items-center gap-1 overflow-x-auto pb-1 sm:gap-2">
        {FASES_ORDEN.map((f, i) => {
          const ordenConocido = idxActual >= 0;
          const completada = ordenConocido && i < idxActual;
          const esActual = ordenConocido && i === idxActual;
          const circulo = completada
            ? "bg-primary text-white"
            : esActual
              ? "bg-primary text-white ring-2 ring-primary ring-offset-2"
              : "border border-neutral-300 bg-white text-neutral-500";
          return (
            <div key={f.code} className="flex items-center gap-1 sm:gap-2">
              <span
                className={`flex h-8 min-w-[2rem] shrink-0 items-center justify-center rounded-full px-2 text-[11px] font-semibold sm:text-xs ${circulo}`}
                title={f.label}
              >
                {f.code}
              </span>
              {i < FASES_ORDEN.length - 1 && (
                <span className="text-[10px] text-neutral-300" aria-hidden>
                  —
                </span>
              )}
            </div>
          );
        })}
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <span className="text-xs text-neutral-600">
          Fase actual:{" "}
          <strong className="text-primary">{fNorm || "—"}</strong>
          {idxActual < 0 && fNorm ? (
            <span className="text-neutral-400"> (código no estándar)</span>
          ) : null}
        </span>
        <button
          type="button"
          className="rounded-md border border-primary bg-white px-3 py-1.5 text-xs font-semibold text-primary transition hover:bg-primary hover:text-white disabled:cursor-not-allowed disabled:opacity-50"
          disabled={procesando || !casoId}
          onClick={() => void aprobar()}
        >
          {procesando ? "Aprobando…" : "Aprobar fase"}
        </button>
      </div>
    </nav>
  );
}
