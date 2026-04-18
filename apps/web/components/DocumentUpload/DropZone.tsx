type DropZoneProps = {
  casoId: string;
};

export function DropZone(_props: DropZoneProps) {
  return <div className="rounded-lg border border-dashed border-neutral-300 p-8" aria-label="Zona de carga" />;
}
