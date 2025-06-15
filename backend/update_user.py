import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
try:
    user = User.objects.get(email='admin@email.com')
    user.is_staff = True
    user.is_superuser = True
    user.set_password('admin')
    user.save()
    print('Usuario actualizado correctamente')
except User.DoesNotExist:
    print('Usuario no encontrado')
except Exception as e:
    print(f'Error: {e}') 