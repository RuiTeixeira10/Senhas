DROP TABLE IF EXISTS tickets;

CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT NOT NULL,
    numero INTEGER NOT NULL,
    codigo TEXT NOT NULL,
    estado TEXT NOT NULL DEFAULT 'emitido',
    hora_chamada TEXT,
    ordem_chamada INTEGER          -- NOVO: define a ordem REAL em que as senhas foram chamadas
);

-- Índices para acelerar as queries mais usadas
CREATE INDEX idx_estado_tipo ON tickets (estado, tipo);
CREATE INDEX idx_ordem_chamada ON tickets (ordem_chamada);