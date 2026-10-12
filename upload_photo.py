"""Upload the included Einstein image fixture as multipart form data.

Run ``python samples/upload_photo.py`` after starting ``server.py``; this
sample uses its documented sandbox token. Importing this script also reads
``assets/einstein.png`` and executes its top-level multipart POST for
``corgi_98231``. This is an executable demonstration, not a reusable Python
API; it defines no public functions or classes, so only this module-level
demonstration is documented. The sandbox returns upload metadata locally.
"""
from pathlib import Path
from client import multipart_file, post

photo_path = Path(__file__).resolve().parents[1] / "assets" / "einstein.png"
photo_body, photo_content_type = multipart_file(
    "photo", photo_path, "image/png", {"pet_id": "corgi_98231"})
post("/pets/upload-photo", body=photo_body, content_type=photo_content_type)
