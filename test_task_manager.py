import pytest
import mysql.connector
from task_manager import pripojeni_db, vytvoreni_tabulky

# Připojení pro testy
def get_test_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ukoly_db"
    )

@pytest.fixture(scope="module", autouse=True)
def setup_teardown():
    vytvoreni_tabulky()
    yield
    # Po testech smažeme testovací úkoly
    conn = get_test_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly WHERE nazev LIKE 'TEST%';")
    conn.commit()
    cursor.close()
    conn.close()

# --- TESTY PRO PRIDANI ---
def test_pridat_ukol_valid():
    conn = get_test_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES ('TEST Úkol', 'Popis testu')")
    conn.commit()
    cursor.execute("SELECT * FROM ukoly WHERE nazev='TEST Úkol'")
    result = cursor.fetchone()
    assert result is not None
    cursor.close()
    conn.close()

def test_pridat_ukol_invalid():
    with pytest.raises(mysql.connector.errors.IntegrityError):
        conn = get_test_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES ('', '')")
        conn.commit()
        cursor.close()
        conn.close()

# --- TESTY PRO AKTUALIZACI ---
def test_aktualizace_valid():
    conn = get_test_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES ('TEST Aktualizace', 'Popis')")
    conn.commit()
    cursor.execute("SELECT id FROM ukoly WHERE nazev='TEST Aktualizace'")
    id_ukolu = cursor.fetchone()[0]
    cursor.execute("UPDATE ukoly SET stav='Hotovo' WHERE id=%s", (id_ukolu,))
    conn.commit()
    cursor.execute("SELECT stav FROM ukoly WHERE id=%s", (id_ukolu,))
    assert cursor.fetchone()[0] == "Hotovo"
    cursor.close()
    conn.close()

def test_aktualizace_invalid():
    conn = get_test_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE ukoly SET stav='Neexistuje' WHERE id=0")
    conn.rollback()
    cursor.close()
    conn.close()

# --- TESTY PRO ODSTRANENI ---
def test_odstranit_valid():
    conn = get_test_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES ('TEST Smazání', 'Popis')")
    conn.commit()
    cursor.execute("SELECT id FROM ukoly WHERE nazev='TEST Smazání'")
    id_ukolu = cursor.fetchone()[0]
    cursor.execute("DELETE FROM ukoly WHERE id=%s", (id_ukolu,))
    conn.commit()
    cursor.execute("SELECT * FROM ukoly WHERE id=%s", (id_ukolu,))
    assert cursor.fetchone() is None
    cursor.close()
    conn.close()

def test_odstranit_invalid():
    conn = get_test_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly WHERE id=-1")  # ID neexistuje
    conn.commit()
    assert cursor.rowcount == 0
    cursor.close()
    conn.close()
