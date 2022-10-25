import os

from google.cloud import storage
from werkzeug.datastructures import FileStorage


ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}

def get_filename(file: FileStorage | str) -> str:
    """
    Gets the string representation of file path i.e. /usr/folder/image.jpg
    Args:
        file: FileStorage object or file path uploaded by user
    Returns:
        string file path
    """
    if isinstance(file, FileStorage):
        return file.filename
    return file


def get_basename(file: FileStorage | str) -> str:
    """
    Gets the basename from a file. i.e. given /usr/folder/image.jpg
    returns image.jpg
    Args:
        file: FileStorage object or file path uploaded by user
    Returns:
        basename from the file path
    """
    return os.path.split(get_filename(file))[1]


def get_extension(file: FileStorage | str) -> str:
    """
    Gets the extension from a file path
    Args:
        file: FileStorage object or file path uploaded by user
    Returns:
        extension type from a file
    """
    return os.path.splitext(get_filename(file))[1].lower()


def allowed_file(file: FileStorage | str) -> bool:
    if get_extension(file) in ALLOWED_EXTENSIONS:
        return True
    return False


def upload_file(bucket_name: str, upload_file: FileStorage, destination: str) -> str:
    """
    Uploads a file from a string to a gcs bucket
    Args:
        bucket_name: name of gcs bucket
        upload_file: file contents to be uploaded
        destination: path to image upload in bucket
    Returns:
        public url to view storage file
    """
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blob = bucket.blob(destination)
    blob.upload_from_string(upload_file.read(), content_type=upload_file.content_type)

    blob.make_public()

    return blob.public_url
