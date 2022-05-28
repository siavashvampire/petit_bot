from telegram import PhotoSize, Document

from MainCode import parent_path


def download_photo(photo: PhotoSize, path: str):
    files = photo.get_file()
    path_temp = parent_path.joinpath(path)
    file = files.download(str(path_temp))
    return path_temp.joinpath(file)


def download_document(document: Document, path: str):
    path_temp = parent_path.joinpath(path + document.file_name)
    file = document.get_file()
    file = file.download(str(path_temp))
    return path_temp.joinpath(file)
