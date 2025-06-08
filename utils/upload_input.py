import os
import uuid

def upload_and_save_image(uploaded_file):
    os.makedirs("static", exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join("static", f"{file_id}_{uploaded_file.name}")
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    return file_path
