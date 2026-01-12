import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT setval('users_id_seq', (SELECT COALESCE(MAX(id), 1) FROM users));")
    print("Secuencia de IDs de usuarios reseteada correctamente")
