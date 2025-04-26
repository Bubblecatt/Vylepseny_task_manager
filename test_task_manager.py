import mysql.connector
from datetime import datetime

# 1. Připojení k databázi
def pripojeni_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",       # změň dle své konfigurace
            password="",       # změň dle své konfigurace
            database="ukoly_db"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Chyba při připojování k databázi: {err}")
        return None

# 2. Vytvoření tabulky
def vytvoreni_tabulky():
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav ENUM('Nezahájeno', 'Probíhá', 'Hotovo') DEFAULT 'Nezahájeno',
                datum_vytvoreni DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cursor.close()
        conn.close()

# 3. Přidání úkolu
def pridat_ukol():
    nazev = input("Zadejte název úkolu: ").strip()
    popis = input("Zadejte popis úkolu: ").strip()

    if not nazev or not popis:
        print("Název i popis jsou povinné!")
        return

    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis) VALUES (%s, %s)", (nazev, popis))
        conn.commit()
        print("Úkol byl přidán.")
        cursor.close()
        conn.close()

# 4. Zobrazení úkolů
def zobrazit_ukoly():
    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN ('Nezahájeno', 'Probíhá')")
        rows = cursor.fetchall()
        if not rows:
            print("Žádné úkoly k zobrazení.")
        else:
            for r in rows:
                print(f"{r[0]} | {r[1]} | {r[2]} | {r[3]}")
        cursor.close()
        conn.close()

# 5. Aktualizace úkolu
def aktualizovat_ukol():
    zobrazit_ukoly()
    id_ukolu = input("Zadejte ID úkolu pro změnu stavu: ")
    novy_stav = input("Zadejte nový stav (Probíhá/Hotovo): ").strip()

    if novy_stav not in ["Probíhá", "Hotovo"]:
        print("Neplatný stav!")
        return

    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        if cursor.fetchone() is None:
            print("Úkol s tímto ID neexistuje.")
        else:
            cursor.execute("UPDATE ukoly SET stav = %s WHERE id = %s", (novy_stav, id_ukolu))
            conn.commit()
            print("Stav úkolu byl aktualizován.")
        cursor.close()
        conn.close()

# 6. Odstranění úkolu
def odstranit_ukol():
    zobrazit_ukoly()
    id_ukolu = input("Zadejte ID úkolu k odstranění: ")

    conn = pripojeni_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ukoly WHERE id = %s", (id_ukolu,))
        if cursor.fetchone() is None:
            print("Úkol s tímto ID neexistuje.")
        else:
            cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
            conn.commit()
            print("Úkol byl odstraněn.")
        cursor.close()
        conn.close()

# 7. Hlavní menu
def hlavni_menu():
    vytvoreni_tabulky()
    while True:
        print("\n--- Hlavní menu ---")
        print("1. Přidat úkol")
        print("2. Zobrazit úkoly")
        print("3. Aktualizovat úkol")
        print("4. Odstranit úkol")
        print("5. Ukončit program")

        volba = input("Vyberte možnost: ")

        if volba == "1":
            pridat_ukol()
        elif volba == "2":
            zobrazit_ukoly()
        elif volba == "3":
            aktualizovat_ukol()
        elif volba == "4":
            odstranit_ukol()
        elif volba == "5":
            print("Program ukončen.")
            break
        else:
            print("Neplatná volba, zkuste znovu.")

if __name__ == "__main__":
    hlavni_menu()
