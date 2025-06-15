import os
from uuid import uuid4

def user_directory_path(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    filename = f"{uuid4().hex}{ext}"
    return os.path.join('utilizadores', str(instance.id), filename)