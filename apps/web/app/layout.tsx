import type { Metadata } from "next";
import { Inter } from "next/font/google";
import { getServerSession } from "next-auth/next";
import "./globals.css";
import { Providers } from "./providers";
import { authOptions } from "@/lib/auth";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: "LUMI Judicial",
  description: "Plataforma de inteligencia jurídica",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await getServerSession(authOptions);

  return (
    <html lang="es" className={inter.variable}>
      <body className="min-h-screen bg-white font-sans text-neutral-900 antialiased">
        <Providers session={session}>{children}</Providers>
      </body>
    </html>
  );
}
