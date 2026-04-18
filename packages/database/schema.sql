-- LUMI Judicial — esquema base de datos (Brief 3.3, tarea S0.4)
-- Ejecutar en Supabase (PostgreSQL) antes de rls_policies.sql y seed_jurisprudencia.sql

SET client_encoding = 'UTF8';

CREATE EXTENSION IF NOT EXISTS vector;

-- ---------------------------------------------------------------------------
-- 1. casos
-- ---------------------------------------------------------------------------
CREATE TABLE public.casos (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id uuid NOT NULL REFERENCES auth.users (id) ON DELETE CASCADE,
    nombre_caso text NOT NULL,
    tipo_accion text NOT NULL CHECK (
        tipo_accion IN (
            'ejecutivo',
            'tutela',
            'laboral',
            'nulidad_restablecimiento',
            'reparacion_directa',
            'otro'
        )
    ),
    estado text NOT NULL DEFAULT 'activo' CHECK (estado IN ('activo', 'pausado', 'cerrado')),
    fase_actual text NOT NULL DEFAULT '0E',
    tokens_consumidos integer NOT NULL DEFAULT 0 CHECK (tokens_consumidos >= 0),
    costo_usd numeric(14, 6) NOT NULL DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_casos_user_id ON public.casos (user_id);
CREATE INDEX idx_casos_estado ON public.casos (estado);

-- ---------------------------------------------------------------------------
-- 2. partes
-- ---------------------------------------------------------------------------
CREATE TABLE public.partes (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id uuid NOT NULL REFERENCES public.casos (id) ON DELETE CASCADE,
    nombre text NOT NULL,
    rol text NOT NULL CHECK (rol IN ('demandante', 'demandado', 'otro')),
    datos_extra jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_partes_caso_id ON public.partes (caso_id);

-- ---------------------------------------------------------------------------
-- 3. hechos (embedding 1536)
-- ---------------------------------------------------------------------------
CREATE TABLE public.hechos (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id uuid NOT NULL REFERENCES public.casos (id) ON DELETE CASCADE,
    fase_origen text NOT NULL,
    contenido text NOT NULL,
    estatus_epistemico text NOT NULL CHECK (
        estatus_epistemico IN ('verificado', 'inferido', 'desconocido', 'contradicho')
    ),
    fuente text,
    embedding vector(1536),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_hechos_caso_id ON public.hechos (caso_id);
CREATE INDEX idx_hechos_embedding ON public.hechos USING hnsw (embedding vector_cosine_ops);

-- ---------------------------------------------------------------------------
-- 4. documentos (embedding 1536)
-- ---------------------------------------------------------------------------
CREATE TABLE public.documentos (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id uuid NOT NULL REFERENCES public.casos (id) ON DELETE CASCADE,
    nombre_original text NOT NULL,
    mime_type text NOT NULL,
    tipo_detectado text,
    estado text NOT NULL DEFAULT 'pendiente' CHECK (
        estado IN ('pendiente', 'procesando', 'listo', 'error')
    ),
    texto_extraido text,
    storage_path text,
    embedding vector(1536),
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_documentos_caso_id ON public.documentos (caso_id);
CREATE INDEX idx_documentos_embedding ON public.documentos USING hnsw (embedding vector_cosine_ops);

-- ---------------------------------------------------------------------------
-- 5. sesiones
-- ---------------------------------------------------------------------------
CREATE TABLE public.sesiones (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id uuid NOT NULL REFERENCES public.casos (id) ON DELETE CASCADE,
    rol text NOT NULL,
    contenido text NOT NULL,
    fase text,
    metadatos jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_sesiones_caso_id_created ON public.sesiones (caso_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- 6. outputs_fases
-- ---------------------------------------------------------------------------
CREATE TABLE public.outputs_fases (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id uuid NOT NULL REFERENCES public.casos (id) ON DELETE CASCADE,
    fase text NOT NULL,
    version integer NOT NULL CHECK (version >= 1),
    contenido jsonb NOT NULL DEFAULT '{}'::jsonb,
    aprobado_abogado boolean NOT NULL DEFAULT false,
    anotaciones text,
    tokens_usados integer NOT NULL DEFAULT 0 CHECK (tokens_usados >= 0),
    costo_usd numeric(14, 6) NOT NULL DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT uq_outputs_fases_caso_fase_version UNIQUE (caso_id, fase, version)
);

CREATE INDEX idx_outputs_fases_caso_id ON public.outputs_fases (caso_id);

-- ---------------------------------------------------------------------------
-- 7. jurisprudencia (embedding 1536)
-- ---------------------------------------------------------------------------
CREATE TABLE public.jurisprudencia (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    cita text NOT NULL,
    titulo text,
    sumario text,
    texto_embeddable text NOT NULL,
    tribunal text,
    fecha_sentencia date,
    embedding vector(1536),
    metadatos jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_jurisprudencia_embedding ON public.jurisprudencia USING hnsw (embedding vector_cosine_ops);

-- ---------------------------------------------------------------------------
-- 8. trazabilidad
-- ---------------------------------------------------------------------------
CREATE TABLE public.trazabilidad (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    caso_id uuid NOT NULL REFERENCES public.casos (id) ON DELETE CASCADE,
    agente text NOT NULL,
    modelo text NOT NULL,
    tokens_input integer NOT NULL DEFAULT 0 CHECK (tokens_input >= 0),
    tokens_output integer NOT NULL DEFAULT 0 CHECK (tokens_output >= 0),
    duracion_ms integer NOT NULL DEFAULT 0 CHECK (duracion_ms >= 0),
    costo_usd numeric(14, 6) NOT NULL DEFAULT 0,
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE INDEX idx_trazabilidad_caso_id_created ON public.trazabilidad (caso_id, created_at DESC);

-- ---------------------------------------------------------------------------
-- RPC: búsqueda semántica de hechos por caso (Brief / motor de contexto)
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION public.match_hechos(
    query_embedding vector(1536),
    p_caso_id uuid,
    match_count integer
)
RETURNS SETOF public.hechos
LANGUAGE sql
STABLE
AS $$
    SELECT h.*
    FROM public.hechos AS h
    WHERE h.caso_id = p_caso_id
      AND h.embedding IS NOT NULL
    ORDER BY h.embedding <=> query_embedding
    LIMIT match_count;
$$;

-- ---------------------------------------------------------------------------
-- Row Level Security (activar; las políticas en rls_policies.sql)
-- ---------------------------------------------------------------------------
ALTER TABLE public.casos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.partes ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.hechos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.documentos ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.sesiones ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.outputs_fases ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.jurisprudencia ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.trazabilidad ENABLE ROW LEVEL SECURITY;
