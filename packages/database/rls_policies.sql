-- LUMI Judicial — políticas RLS (S0.4)
-- Requiere haber aplicado schema.sql (tablas creadas y RLS activado sin políticas aún).

-- ---------------------------------------------------------------------------
-- Permisos base para el rol autenticado (PostgREST / cliente con JWT)
-- ---------------------------------------------------------------------------
GRANT USAGE ON SCHEMA public TO authenticated;

GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.casos TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.partes TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.hechos TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.documentos TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.sesiones TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.outputs_fases TO authenticated;
GRANT SELECT ON TABLE public.jurisprudencia TO authenticated;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE public.trazabilidad TO authenticated;

GRANT EXECUTE ON FUNCTION public.match_hechos(vector, uuid, integer) TO authenticated;

-- ---------------------------------------------------------------------------
-- 1. casos — solo el propietario (user_id = auth.uid())
-- ---------------------------------------------------------------------------
CREATE POLICY casos_owner_all
    ON public.casos
    FOR ALL
    TO authenticated
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- ---------------------------------------------------------------------------
-- 2. partes — acceso vía propiedad del caso
-- ---------------------------------------------------------------------------
CREATE POLICY partes_via_caso_owner
    ON public.partes
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = partes.caso_id
              AND c.user_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = partes.caso_id
              AND c.user_id = auth.uid()
        )
    );

-- ---------------------------------------------------------------------------
-- 3. hechos
-- ---------------------------------------------------------------------------
CREATE POLICY hechos_via_caso_owner
    ON public.hechos
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = hechos.caso_id
              AND c.user_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = hechos.caso_id
              AND c.user_id = auth.uid()
        )
    );

-- ---------------------------------------------------------------------------
-- 4. documentos
-- ---------------------------------------------------------------------------
CREATE POLICY documentos_via_caso_owner
    ON public.documentos
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = documentos.caso_id
              AND c.user_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = documentos.caso_id
              AND c.user_id = auth.uid()
        )
    );

-- ---------------------------------------------------------------------------
-- 5. sesiones
-- ---------------------------------------------------------------------------
CREATE POLICY sesiones_via_caso_owner
    ON public.sesiones
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = sesiones.caso_id
              AND c.user_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = sesiones.caso_id
              AND c.user_id = auth.uid()
        )
    );

-- ---------------------------------------------------------------------------
-- 6. outputs_fases
-- ---------------------------------------------------------------------------
CREATE POLICY outputs_fases_via_caso_owner
    ON public.outputs_fases
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = outputs_fases.caso_id
              AND c.user_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = outputs_fases.caso_id
              AND c.user_id = auth.uid()
        )
    );

-- ---------------------------------------------------------------------------
-- 7. jurisprudencia — catálogo de lectura (sin caso_id)
-- ---------------------------------------------------------------------------
CREATE POLICY jurisprudencia_read_all
    ON public.jurisprudencia
    FOR SELECT
    TO authenticated
    USING (true);

-- ---------------------------------------------------------------------------
-- 8. trazabilidad
-- ---------------------------------------------------------------------------
CREATE POLICY trazabilidad_via_caso_owner
    ON public.trazabilidad
    FOR ALL
    TO authenticated
    USING (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = trazabilidad.caso_id
              AND c.user_id = auth.uid()
        )
    )
    WITH CHECK (
        EXISTS (
            SELECT 1
            FROM public.casos AS c
            WHERE c.id = trazabilidad.caso_id
              AND c.user_id = auth.uid()
        )
    );
