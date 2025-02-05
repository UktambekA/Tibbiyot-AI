from datetime import datetime
import time, sqlite3

def check_notifications():
    conn = sqlite3.connect('health_app.db')
    cursor = conn.cursor()
    cursor.execute("""
    SELECT medicine_name, reminder_time FROM Medications
    """)
    medications = cursor.fetchall()
    conn.close()
    
    current_time = datetime.now().strftime('%H:%M')
    for med in medications:
        if med[1] == current_time:
            print(f"Eslatma: {med[0]} ichish vaqti!")
    time.sleep(60)  # Har 1 minutda tekshirish
