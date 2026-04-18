export default function CasoLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <div className="min-h-screen">
      <header className="border-b border-neutral-200 bg-neutral-50 px-4 py-3">
        <h2 className="text-sm font-medium text-primary">Caso</h2>
      </header>
      {children}
    </div>
  );
}
