import sqlite3
import os
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "tickets.db")


@contextmanager
def get_connection():
    """
    Context manager para a ligação à BD.
    Garante que a ligação é sempre fechada, mesmo se ocorrer um erro.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def get_next_number(tipo):
    """Obtém o próximo número sequencial para um tipo de senha (G ou P)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(numero) FROM tickets WHERE tipo = ?", (tipo,))
        result = cursor.fetchone()[0]
        return 1 if result is None else result + 1


def inserir_senha(tipo):
    """Regista uma nova senha (G ou P) e devolve o código gerado (ex: G001)."""
    numero = get_next_number(tipo)
    codigo = f"{tipo}{str(numero).zfill(3)}"

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tickets (tipo, numero, codigo, estado)
            VALUES (?, ?, ?, 'emitido')
        """, (tipo, numero, codigo))

    return codigo


def proxima_senha():
    """
    Devolve a próxima senha a chamar (id, codigo).
    Prioridade (P) é sempre atendida antes de Geral (G), respeitando a ordem
    de chegada dentro de cada tipo (numero ASC).
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, codigo FROM tickets
            WHERE estado = 'emitido' AND tipo = 'P'
            ORDER BY numero ASC
            LIMIT 1
        """)
        prioridade = cursor.fetchone()
        if prioridade:
            return prioridade

        cursor.execute("""
            SELECT id, codigo FROM tickets
            WHERE estado = 'emitido' AND tipo = 'G'
            ORDER BY numero ASC
            LIMIT 1
        """)
        return cursor.fetchone()


def chamar_senha(id_senha):
    """
    Marca uma senha como 'chamado' e regista a sua ORDEM REAL de chamada.

    IMPORTANTE: usamos um contador dedicado (ordem_chamada) em vez do 'id'
    da senha. O 'id' reflete a ordem em que a senha foi EMITIDA, não a ordem
    em que foi CHAMADA -- e são coisas diferentes, especialmente com
    prioridades a "furarem" a fila. Foi esta confusão que causava o bug em
    que o painel ficava preso numa senha prioritária antiga em vez de
    avançar para uma senha Geral chamada mais recentemente.
    """
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(ordem_chamada) FROM tickets")
        max_ordem = cursor.fetchone()[0]
        nova_ordem = 1 if max_ordem is None else max_ordem + 1

        cursor.execute("""
            UPDATE tickets
            SET estado = 'chamado',
                hora_chamada = CURRENT_TIMESTAMP,
                ordem_chamada = ?
            WHERE id = ?
        """, (nova_ordem, id_senha))


def ultima_chamada():
    """
    Devolve o código da ÚLTIMA senha chamada (a mais recente),
    baseado na ordem real de chamada -- não no id de emissão.
    """
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT codigo FROM tickets
            WHERE estado = 'chamado'
            ORDER BY ordem_chamada DESC
            LIMIT 1
        """)
        resultado = cursor.fetchone()
        return resultado[0] if resultado else None


def listar_tickets(estado=None):
    """Função auxiliar de diagnóstico: lista tickets (todos ou por estado)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        if estado:
            cursor.execute("""
                SELECT id, tipo, numero, codigo, estado, ordem_chamada
                FROM tickets WHERE estado = ? ORDER BY id
            """, (estado,))
        else:
            cursor.execute("""
                SELECT id, tipo, numero, codigo, estado, ordem_chamada
                FROM tickets ORDER BY id
            """)
        return cursor.fetchall()


def limpar_tickets():
    """Apaga todas as senhas. Útil para reiniciar o sistema num novo dia."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tickets")