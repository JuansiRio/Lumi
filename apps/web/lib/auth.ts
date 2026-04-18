import type { NextAuthOptions } from "next-auth";
import EmailProvider from "next-auth/providers/email";

/**
 * Configuración mínima de NextAuth (S0.2 — sin lógica de negocio).
 * Las variables de entorno reales se documentan en .env.example (tareas posteriores).
 */
export const authOptions: NextAuthOptions = {
  providers: [
    EmailProvider({
      server: process.env.EMAIL_SERVER ?? "",
      from: process.env.EMAIL_FROM ?? "noreply@localhost",
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET ?? "dev-placeholder-secret-change-in-production-32chars",
  session: { strategy: "jwt" },
};
