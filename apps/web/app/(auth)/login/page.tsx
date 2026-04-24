"use client";

import { useState, type FormEvent } from "react";
import { signIn } from "next-auth/react";

const PRIMARY = "#1F4E79";

export default function LoginPage() {
  const [email, setEmail] = useState("");
  const [success, setSuccess] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setAuthError(null);
    setSuccess(false);
    setLoading(true);
    try {
      const res = await signIn("email", {
        email: email.trim(),
        redirect: false,
        callbackUrl: "/",
      });
      if (res?.error === "AccessDenied") {
        setAuthError("Este correo no está autorizado para acceder.");
        return;
      }
      if (res?.error) {
        setAuthError("No se pudo enviar el enlace. Inténtalo de nuevo.");
        return;
      }
      if (res?.ok) {
        setSuccess(true);
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-slate-50 px-4 py-12">
      <div className="w-full max-w-md space-y-8 rounded-2xl border border-slate-200 bg-white p-8 shadow-sm">
        <header className="space-y-2 text-center">
          <h1 className="text-3xl font-bold tracking-tight text-[#1F4E79]">
            LUMI Judicial
          </h1>
          <p className="text-base text-neutral-600">
            Asistente de inteligencia jurídica
          </p>
        </header>

        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <label htmlFor="email" className="sr-only">
              Correo electrónico
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="tu@email.com"
              className="w-full rounded-lg border border-slate-300 px-4 py-3 text-neutral-900 shadow-sm outline-none ring-[#1F4E79] transition placeholder:text-neutral-400 focus:border-[#1F4E79] focus:ring-2"
              disabled={loading}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg px-4 py-3 font-semibold text-white shadow-sm transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-60"
            style={{ backgroundColor: PRIMARY }}
          >
            {loading ? "Enviando…" : "Enviar Magic Link"}
          </button>

          {success ? (
            <p
              className="text-center text-sm font-medium text-[#1F4E79]"
              role="status"
            >
              Revisa tu correo
            </p>
          ) : null}

          {authError ? (
            <p className="text-center text-sm font-medium text-red-600" role="alert">
              {authError}
            </p>
          ) : null}
        </form>
      </div>
    </main>
  );
}
