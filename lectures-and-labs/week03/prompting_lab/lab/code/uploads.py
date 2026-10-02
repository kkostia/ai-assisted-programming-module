"""Saving files that users upload: the subject of DIY 4.

save_upload(filename, data) stores the bytes a user uploaded, under the
name the user's browser sent, in UPLOAD_DIR.
"""
import os

UPLOAD_DIR = "uploads"


def save_upload(filename, data):
    """Save the uploaded bytes in UPLOAD_DIR and return the path written."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    upload_dir = os.path.realpath(UPLOAD_DIR)
    path = os.path.realpath(os.path.join(upload_dir, filename))
    if os.path.commonpath((upload_dir, path)) != upload_dir:
        raise ValueError("Upload path must stay inside UPLOAD_DIR")
    f = open(path, "wb")
    f.write(data)
    f.close()
    return path
