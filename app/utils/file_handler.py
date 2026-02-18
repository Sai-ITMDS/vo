import os
import uuid
import tempfile


def save_temp_file(content, suffix):

    filename = f"{uuid.uuid4()}{suffix}"

    path = os.path.join(
        tempfile.gettempdir(),
        filename
    )

    with open(path, "wb") as f:

        f.write(content)

    return path


def delete_file(path):

    if os.path.exists(path):

        os.remove(path)
