-- NextAuth.js / Auth.js — esquema `next_auth` para @auth/supabase-adapter
-- Referencia: https://authjs.dev/getting-started/adapters/supabase
--
-- Ejecutar en el SQL Editor de Supabase (o vía migración CLI).
-- Requisito: extensión para uuid_generate_v4().
-- El adaptador usa createClient(..., { db: { schema: "next_auth" } }).

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Name: next_auth; Type: SCHEMA;
CREATE SCHEMA IF NOT EXISTS next_auth;

GRANT USAGE ON SCHEMA next_auth TO service_role;
GRANT ALL ON SCHEMA next_auth TO postgres;

-- users
CREATE TABLE IF NOT EXISTS next_auth.users
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    name text,
    email text,
    "emailVerified" timestamp with time zone,
    image text,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT email_unique UNIQUE (email)
);

GRANT ALL ON TABLE next_auth.users TO postgres;
GRANT ALL ON TABLE next_auth.users TO service_role;

-- Función usada en políticas RLS avanzadas (p. ej. tablas en public vinculadas a next_auth.users)
CREATE OR REPLACE FUNCTION next_auth.uid() RETURNS uuid
    LANGUAGE sql
    STABLE
AS $$
  SELECT
    COALESCE(
      NULLIF(current_setting('request.jwt.claim.sub', true), ''),
      (NULLIF(current_setting('request.jwt.claims', true), '')::jsonb ->> 'sub')
    )::uuid
$$;

-- sessions
CREATE TABLE IF NOT EXISTS next_auth.sessions
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    expires timestamp with time zone NOT NULL,
    "sessionToken" text NOT NULL,
    "userId" uuid,
    CONSTRAINT sessions_pkey PRIMARY KEY (id),
    CONSTRAINT sessionToken_unique UNIQUE ("sessionToken"),
    CONSTRAINT "sessions_userId_fkey" FOREIGN KEY ("userId")
        REFERENCES next_auth.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

GRANT ALL ON TABLE next_auth.sessions TO postgres;
GRANT ALL ON TABLE next_auth.sessions TO service_role;

-- accounts
CREATE TABLE IF NOT EXISTS next_auth.accounts
(
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    type text NOT NULL,
    provider text NOT NULL,
    "providerAccountId" text NOT NULL,
    refresh_token text,
    access_token text,
    expires_at bigint,
    token_type text,
    scope text,
    id_token text,
    session_state text,
    oauth_token_secret text,
    oauth_token text,
    "userId" uuid,
    CONSTRAINT accounts_pkey PRIMARY KEY (id),
    CONSTRAINT provider_unique UNIQUE (provider, "providerAccountId"),
    CONSTRAINT "accounts_userId_fkey" FOREIGN KEY ("userId")
        REFERENCES next_auth.users (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
);

GRANT ALL ON TABLE next_auth.accounts TO postgres;
GRANT ALL ON TABLE next_auth.accounts TO service_role;

-- verification_tokens
CREATE TABLE IF NOT EXISTS next_auth.verification_tokens
(
    identifier text,
    token text,
    expires timestamp with time zone NOT NULL,
    CONSTRAINT verification_tokens_pkey PRIMARY KEY (token),
    CONSTRAINT token_unique UNIQUE (token),
    CONSTRAINT token_identifier_unique UNIQUE (token, identifier)
);

GRANT ALL ON TABLE next_auth.verification_tokens TO postgres;
GRANT ALL ON TABLE next_auth.verification_tokens TO service_role;

-- ---------------------------------------------------------------------------
-- Row Level Security (RLS)
-- El cliente del adaptador usa SUPABASE_SERVICE_ROLE_KEY: en Supabase ese rol
-- suele tener BYPASSRLS, por lo que el adapter sigue funcionando aunque RLS
-- esté activo. Las políticas siguientes permiten explícitamente lectura y
-- escritura a service_role y postgres (conexiones/mantenimiento).
-- Los roles anon/authenticated no reciben políticas: sin acceso por defecto
-- si expones el esquema next_auth en la API (recomendado: solo service role).
-- ---------------------------------------------------------------------------

DROP POLICY IF EXISTS next_auth_users_service_role_all ON next_auth.users;
DROP POLICY IF EXISTS next_auth_users_postgres_all ON next_auth.users;
DROP POLICY IF EXISTS next_auth_sessions_service_role_all ON next_auth.sessions;
DROP POLICY IF EXISTS next_auth_sessions_postgres_all ON next_auth.sessions;
DROP POLICY IF EXISTS next_auth_accounts_service_role_all ON next_auth.accounts;
DROP POLICY IF EXISTS next_auth_accounts_postgres_all ON next_auth.accounts;
DROP POLICY IF EXISTS next_auth_verification_tokens_service_role_all ON next_auth.verification_tokens;
DROP POLICY IF EXISTS next_auth_verification_tokens_postgres_all ON next_auth.verification_tokens;

ALTER TABLE next_auth.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE next_auth.sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE next_auth.accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE next_auth.verification_tokens ENABLE ROW LEVEL SECURITY;

CREATE POLICY next_auth_users_service_role_all
  ON next_auth.users
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY next_auth_users_postgres_all
  ON next_auth.users
  FOR ALL
  TO postgres
  USING (true)
  WITH CHECK (true);

CREATE POLICY next_auth_sessions_service_role_all
  ON next_auth.sessions
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY next_auth_sessions_postgres_all
  ON next_auth.sessions
  FOR ALL
  TO postgres
  USING (true)
  WITH CHECK (true);

CREATE POLICY next_auth_accounts_service_role_all
  ON next_auth.accounts
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY next_auth_accounts_postgres_all
  ON next_auth.accounts
  FOR ALL
  TO postgres
  USING (true)
  WITH CHECK (true);

CREATE POLICY next_auth_verification_tokens_service_role_all
  ON next_auth.verification_tokens
  FOR ALL
  TO service_role
  USING (true)
  WITH CHECK (true);

CREATE POLICY next_auth_verification_tokens_postgres_all
  ON next_auth.verification_tokens
  FOR ALL
  TO postgres
  USING (true)
  WITH CHECK (true);
