import os
from uuid import uuid4

def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('utilizadores', str(instance.id), filename)


def product_image_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('produtos', str(instance.id), filename)
