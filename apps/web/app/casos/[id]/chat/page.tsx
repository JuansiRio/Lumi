"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useCallback, useEffect, useState, type ChangeEventHandler } from "react";

import { ChatWindow } from "@/components/Chat/ChatWindow";
import { FaseIndicator } from "@/components/Chat/FaseIndicator";
import { MessageInput } from "@/components/Chat/MessageInput";
import type { Caso, Documento } from "@/lib/api-client";
import { downloadBorrador, getCaso, listDocumentos, postDocumento } from "@/lib/api-client";

export default function ChatPage() {
  const params = useParams();
  const casoId = typeof params?.id === "string" ? params.id : "";

  const [caso, setCaso] = useState<Caso | null>(null);
  const [docs, setDocs] = useState<Documento[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [refreshChat, setRefreshChat] = useState(0);

  const recargarCaso = useCallback(async () => {
    if (!casoId) {
      return;
    }
    try {
      const c = await getCaso(casoId);
      setCaso(c);
      setError(null);
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo cargar el caso.");
    }
  }, [casoId]);

  const recargarDocumentos = useCallback(async () => {
    if (!casoId) {
      return;
    }
    try {
      const d = await listDocumentos(casoId);
      setDocs(d);
    } catch {
      /* silencioso en polling */
    }
  }, [casoId]);

  useEffect(() => {
    void recargarCaso();
  }, [recargarCaso]);

  useEffect(() => {
    if (!casoId) {
      return;
    }
    void recargarDocumentos();
    const id = window.setInterval(() => {
      void recargarDocumentos();
    }, 2000);
    return () => window.clearInterval(id);
  }, [casoId, recargarDocumentos]);

  const bumpChat = () => setRefreshChat((n) => n + 1);

  const subirArchivo: ChangeEventHandler<HTMLInputElement> = async (e) => {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file || !casoId) {
      return;
    }
    try {
      await postDocumento(casoId, file);
      void recargarDocumentos();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Error al subir el documento.");
    }
  };

  const borrador = async () => {
    if (!casoId) {
      return;
    }
    try {
      await downloadBorrador(casoId);
    } catch (err) {
      setError(err instanceof Error ? err.message : "No se pudo descargar el borrador.");
    }
  };

  return (
    <main className="flex min-h-screen flex-col bg-neutral-100">
      <header className="flex flex-wrap items-center justify-between gap-2 border-b border-neutral-200 bg-white px-4 py-3">
        <div className="flex items-center gap-3">
          <Link href="/casos" className="text-sm font-medium text-primary hover:underline">
            ← Casos
          </Link>
          <h1 className="text-lg font-semibold text-neutral-900">
            {caso?.nombre_caso ?? "Chat"}
          </h1>
        </div>
        <div className="flex flex-wrap items-center gap-2">
          <label className="cursor-pointer rounded-md border border-neutral-300 bg-white px-3 py-1.5 text-xs font-medium text-neutral-700 hover:bg-neutral-50">
            Subir documento
            <input type="file" className="hidden" accept=".pdf,.doc,.docx,.png,.jpg,.jpeg,.webp" onChange={subirArchivo} />
          </label>
          <button
            type="button"
            className="rounded-md border border-primary bg-white px-3 py-1.5 text-xs font-semibold text-primary hover:bg-primary hover:text-white"
            onClick={() => void borrador()}
          >
            Borrador .docx
          </button>
        </div>
      </header>

      <FaseIndicator
        casoId={casoId}
        faseActual={caso?.fase_actual ?? ""}
        onFaseChanged={() => {
          void recargarCaso();
          bumpChat();
        }}
      />

      {error && (
        <div className="bg-red-50 px-4 py-2 text-sm text-red-800" role="alert">
          {error}
        </div>
      )}

      <section className="border-b border-neutral-200 bg-white px-4 py-2 text-xs text-neutral-600" aria-live="polite">
        <span className="font-semibold text-primary">Documentos</span>
        {docs.length === 0 ? (
          <span className="ml-2">Ninguno aún.</span>
        ) : (
          <ul className="mt-1 flex flex-wrap gap-2">
            {docs.map((d) => (
              <li key={d.id} className="rounded bg-neutral-100 px-2 py-0.5">
                {d.nombre_original}{" "}
                <span className="text-neutral-400">({d.estado})</span>
              </li>
            ))}
          </ul>
        )}
      </section>

      <div className="flex min-h-0 flex-1 flex-col">
        <ChatWindow casoId={casoId} refreshTrigger={refreshChat} />
        <MessageInput casoId={casoId} onMessageSent={bumpChat} />
      </div>
    </main>
  );
}
