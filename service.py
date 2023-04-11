import os

from fastapi import UploadFile, File
from loguru import logger

from Storage import Storage


def save_file_in_storage(file: UploadFile = File(...)):
    try:
        # Читаем файл, который пришёл в запросе
        contents = file.file.read()

        # Сохраняем его во временную папку, чуть попозже удалим оттуда
        with open('tmp_files/' + file.filename, 'wb') as f:
            f.write(contents)

        # Сохраняем в Яндекс storage с получением ссылки на файл
        s3 = Storage('profile-pictures')
        file_url = s3.save_file(file.filename)
    except Exception as e:
        logger.error(f'Возникла ошибка при сохранении файла\n'
                     f'{e}')
        raise e
    finally:
        # Закрываем чтение файла и удаляем локальную версию, если она есть
        file.file.close()
        if os.path.isfile('tmp_files/' + file.filename):
            os.remove('tmp_files/' + file.filename)
    return file_url
