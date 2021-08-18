import urllib.request as request
from pathlib import Path
import zipfile
from caddiepy import settings


def download_file_ftp(filename, filepath):
    Path(settings.PATH_SOTRAGE).mkdir(parents=True, exist_ok=True)

    request.urlretrieve(filepath, f'{settings.PATH_SOTRAGE}/{filename}')


def unzip(file):
    with zipfile.ZipFile(f'{settings.PATH_SOTRAGE}/{file}', 'r') as zip_ref:
        zip_ref.extractall(f'{settings.PATH_SOTRAGE}/{file[:-4]}')