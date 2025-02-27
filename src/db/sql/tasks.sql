CREATE TABLE IF NOT EXISTS public.tasks
(
    id serial,
    description character varying(30) NOT NULL,
    priority smallint,
    is_completed boolean NOT NULL DEFAULT false,
    CONSTRAINT tasks_pkey PRIMARY KEY (id)
)