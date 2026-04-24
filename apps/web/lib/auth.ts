import type { NextAuthOptions } from "next-auth";
import type { Adapter } from "next-auth/adapters";
import { SupabaseAdapter } from "@auth/supabase-adapter";
import EmailProvider from "next-auth/providers/email";

const resendSmtp = {
  host: "smtp.resend.com",
  port: 465,
  secure: true,
  auth: {
    user: "resend",
    pass: process.env.RESEND_API_KEY ?? "",
  },
};

/**
 * NextAuth + magic link (Resend SMTP) + sesiones en Supabase vía adaptador.
 * Servidor: RESEND_API_KEY, EMAIL_FROM, NEXTAUTH_SECRET,
 * NEXT_PUBLIC_SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY (secreta, no NEXT_PUBLIC).
 * AUTHORIZED_USERS opcional: lista separada por comas de emails permitidos.
 */
export const authOptions: NextAuthOptions = {
  adapter: SupabaseAdapter({
    url: process.env.NEXT_PUBLIC_SUPABASE_URL!,
    secret: process.env.SUPABASE_SERVICE_ROLE_KEY!,
  }) as Adapter,
  providers: [
    EmailProvider({
      server: resendSmtp,
      from: process.env.EMAIL_FROM ?? "noreply@localhost",
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET ?? "dev-placeholder-secret-change-in-production-32chars",
  session: { strategy: "database" },
  callbacks: {
    async signIn({ user }) {
      const raw = process.env.AUTHORIZED_USERS?.trim();
      if (!raw) {
        return true;
      }
      const allowed = raw
        .split(",")
        .map((e) => e.trim().toLowerCase())
        .filter(Boolean);
      const email = user?.email?.toLowerCase() ?? "";
      return allowed.includes(email);
    },
  },
};
