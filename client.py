"""Send JSON and multipart requests for the executable Sprint 06 samples.

The public API consists of :func:`post` and :func:`multipart_file`. Importing
this module reads configuration but does not contact the sandbox. The default
token is a public credential for the local teaching sandbox only. Set
``API_BASE_URL`` and ``API_AUTH_TOKEN`` before import to override the defaults.
"""
import json
import os
from urllib.request import Request, urlopen

#: API prefix, read once at import; endpoint paths are appended without joining.
BASE_URL = os.environ.get("API_BASE_URL", "http://127.0.0.1:8080/v1")
#: Bearer credential, read once at import; the default is local sandbox data.
AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN", "sprint05-local-sandbox")

def post(path, payload=None, *, body=None, content_type="application/json"):
    """POST a request, print its status and JSON response, and return the JSON.

    A non-``None`` ``body`` takes priority over ``payload``, including empty
    bytes. Otherwise ``payload`` is JSON-encoded as UTF-8, even when a different
    content type is supplied. The request uses the configured bearer token and
    a ten-second ``urlopen`` timeout. Response schemas are not validated here.
    HTTP errors propagate before a success record can be printed.

    Args:
        path (str): Endpoint suffix beginning with ``/``, for example
            ``/pets/upload-photo``. Appended directly to :data:`BASE_URL`.
        payload (object | None): JSON-serializable request value. Defaults to
            ``None``, which sends JSON ``null`` when no raw body is provided.
        body (bytes | None): Optional already-encoded request body, such as
            the multipart bytes returned by :func:`multipart_file`.
        content_type (str): Value of the request's ``Content-Type`` header.
            Defaults to ``application/json``; use the generated multipart
            content type when sending a file.

    Returns:
        object: Decoded response JSON, normally a ``dict`` for the sandbox
        endpoints. The return value does not contain the HTTP status. A JSON
        record with ``http_status`` and ``body`` is also printed to stdout.

    Raises:
        TypeError: If ``payload`` cannot be JSON-serialized and no body is
            provided.
        ValueError: If JSON serialization finds a circular reference, or the
            configured URL is invalid.
        urllib.error.HTTPError: If the server returns an HTTP error, including
            validation, authentication, and unsupported-media responses.
        urllib.error.URLError: If opening the URL fails, including connection
            failures. The underlying cause is available as ``reason``.
        TimeoutError: If a socket operation reaches its timeout.
        OSError: If a response read or stdout write fails.
        json.JSONDecodeError: If the response is not valid JSON.
        UnicodeDecodeError: If response bytes cannot be decoded as JSON text.
        UnicodeEncodeError: If stdout cannot represent the printed response.

    Examples:
        Upload the included Einstein PNG using a mocked response. This example
        reads the local fixture and performs no network requests::

            >>> import client
            >>> import io
            >>> import json
            >>> from contextlib import redirect_stdout
            >>> from pathlib import Path
            >>> from unittest.mock import patch
            >>> photo = Path(client.__file__).resolve().parents[1] / "assets" / "einstein.png"
            >>> data, media_type = client.multipart_file(
            ...     "photo", photo, "image/png", {"pet_id": "corgi_98231"})
            >>> expected = {"pet_id": "corgi_98231", "photo_id": "photo_0001",
            ...             "filename": "einstein.png", "bytes_received": photo.stat().st_size}
            >>> response = io.BytesIO(json.dumps(expected).encode("utf-8"))
            >>> response.status = 200
            >>> output = io.StringIO()
            >>> with patch("client.urlopen", return_value=response) as transport:
            ...     with redirect_stdout(output):
            ...         result = client.post("/pets/upload-photo", body=data, content_type=media_type)
            >>> result == expected
            True
            >>> json.loads(output.getvalue())["http_status"]
            200
            >>> transport.call_args.args[0].data == data
            True
    """
    request_body = body if body is not None else json.dumps(payload).encode("utf-8")
    request = Request(BASE_URL + path, data=request_body, method="POST", headers={
        "Authorization": "Bearer " + AUTH_TOKEN, "Content-Type": content_type})
    with urlopen(request, timeout=10) as response:
        response_body = json.load(response)
        print(json.dumps({"http_status": response.status, "body": response_body}, ensure_ascii=False))
        return response_body

def multipart_file(field_name, file_path, media_type, fields):
    """Build a multipart body containing text fields and one complete file.

    Text fields retain mapping iteration order and use their string
    representations. The file follows those fields, and the body ends with a
    closing boundary. The entire file and body are held in memory. The fixed
    boundary and unescaped field names, values, and filename are intended for
    the controlled lab fixtures; this helper does not validate them.

    Args:
        field_name (str): Form field for the file, such as ``photo`` or ``audio``.
        file_path (pathlib.Path): Local file to read. Its ``name`` property is
            used as the multipart filename.
        media_type (str): File-part ``Content-Type``, for example ``image/png``
            or ``audio/wav``. Copied into the body without validation.
        fields (Mapping[str, object]): Additional text form fields, such as
            ``{"pet_id": "corgi_98231"}``; each value is formatted as text.

    Returns:
        tuple[bytes, str]: Complete request body and matching multipart
        ``Content-Type`` header, including the boundary parameter. Pass these
        as ``body`` and ``content_type`` to :func:`post`.

    Raises:
        FileNotFoundError: If ``file_path`` does not exist.
        PermissionError: If the file cannot be read with current permissions.
        OSError: If another filesystem error prevents reading the file.
        UnicodeEncodeError: If a field or filename contains text that cannot
            be encoded as UTF-8.

    Examples:
        Build a Corg.ly Einstein photo request without contacting a server::

            >>> import client
            >>> from pathlib import Path
            >>> photo = Path(client.__file__).resolve().parents[1] / "assets" / "einstein.png"
            >>> data, media_type = client.multipart_file(
            ...     "photo", photo, "image/png", {"pet_id": "corgi_98231"})
            >>> media_type
            'multipart/form-data; boundary=Sprint05MultipartBoundary91'
            >>> b'name="pet_id"\\r\\n\\r\\ncorgi_98231' in data
            True
            >>> b'name="photo"; filename="einstein.png"' in data
            True
            >>> photo.read_bytes() in data
            True
    """
    boundary = "Sprint05MultipartBoundary91"
    parts = []
    for name, value in fields.items():
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{field_name}"; filename="{file_path.name}"\r\nContent-Type: {media_type}\r\n\r\n'.encode())
    parts.extend([file_path.read_bytes(), f"\r\n--{boundary}--\r\n".encode()])
    return b"".join(parts), "multipart/form-data; boundary=" + boundary
