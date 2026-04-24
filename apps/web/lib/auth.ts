import type { NextAuthOptions } from "next-auth";
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
 * NextAuth + magic link por email vía Resend SMTP.
 * RESEND_API_KEY, EMAIL_FROM, NEXTAUTH_SECRET en producción.
 * AUTHORIZED_USERS opcional: lista separada por comas de emails permitidos.
 */
export const authOptions: NextAuthOptions = {
  providers: [
    EmailProvider({
      server: resendSmtp,
      from: process.env.EMAIL_FROM ?? "noreply@localhost",
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET ?? "dev-placeholder-secret-change-in-production-32chars",
  session: { strategy: "jwt" },
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
