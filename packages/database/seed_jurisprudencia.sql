-- LUMI Judicial — semilla mínima de jurisprudencia (ejemplos de referencia)
-- Cinco registros ilustrativos; embedding NULL hasta generación offline / ETL.

INSERT INTO public.jurisprudencia (
    cita,
    titulo,
    sumario,
    texto_embeddable,
    tribunal,
    fecha_sentencia,
    embedding,
    metadatos
)
VALUES
(
    'Corte Constitucional de Colombia, Sentencia T-025 de 2004',
    'Derechos de las personas en situación de desplazamiento forzado',
    'Reafirma el carácter de mínimo vital de ciertos derechos y la obligación estatal de protección diferenciada.',
    'Corte Constitucional T-025/2004: enfoque de protección reforzada y deberes del Estado frente a poblaciones en riesgo. Referencia transversal para análisis de vulnerabilidad en procesos civiles y de familia.',
    'Corte Constitucional',
    '2004-01-22',
    NULL,
    '{"materia": "constitucional", "tema": "minimo_vital"}'::jsonb
),
(
    'Corte Suprema de Justicia, Sala de Casación Civil, 3 de mayo de 2019',
    'Alimentos y prueba del menoscabo',
    'Lineamientos sobre carga probatoria y estándares probatorios en demandas de alimentos.',
    'CSJ Sala Civil, 3 mayo 2019: criterios sobre prueba del menoscabo, necesidad manifiesta y proporcionalidad de la cuota alimentaria en el contexto del interés superior del menor.',
    'Corte Suprema de Justicia — Sala Civil',
    '2019-05-03',
    NULL,
    '{"materia": "familia", "tema": "alimentos"}'::jsonb
),
(
    'Corte Constitucional de Colombia, Sentencia C-092 de 2008',
    'Igualdad y no discriminación en el acceso a la administración de justicia',
    'Desarrollo del principio de igualdad sustantiva en relaciones jurídicas asimétricas.',
    'C-092/2008: igualdad sustantiva, razonabilidad y proporcionalidad; útil como marco argumental en tutelas y defensa de derechos fundamentales en procesos judiciales.',
    'Corte Constitucional',
    '2008-04-02',
    NULL,
    '{"materia": "constitucional", "tema": "igualdad"}'::jsonb
),
(
    'Corte Suprema de Justicia, Sala de Casación Civil, 12 de septiembre de 2018',
    'Liquidación de sentencias y actualización de cuantías',
    'Criterios sobre indexación y actualización monetaria en sentencias de condena al pago.',
    'CSJ Sala Civil, 12 sep 2018: actualización de cuantías, intereses moratorios y liquidación de sentencias ejecutivas; aplicable a litigios de suma y ejecución de obligaciones dinerarias.',
    'Corte Suprema de Justicia — Sala Civil',
    '2018-09-12',
    NULL,
    '{"materia": "civil", "tema": "liquidacion"}'::jsonb
),
(
    'Corte Constitucional de Colombia, Sentencia T-823 de 2011',
    'Derechos de niñas, niños y adolescentes en procesos judiciales',
    'Énfasis en el interés superior de la infancia y la debida protección procesal.',
    'T-823/2011: interés superior del menor, escucha y participación; referencia para fases de estrategia y teoría del caso en controversias de familia y alimentos.',
    'Corte Constitucional',
    '2011-11-09',
    NULL,
    '{"materia": "familia", "tema": "infancia"}'::jsonb
);
