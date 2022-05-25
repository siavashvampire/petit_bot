from telegram import PhotoSize

from MainCode import parent_path


def download_photo(photo: PhotoSize, path: str):
    files = photo.get_file()
    path_temp = parent_path.joinpath(path)
    file = files.download(str(path_temp))
    return file
