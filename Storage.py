import boto3
from loguru import logger


# Идентификатор ключа:
# YCAJE4Vn2tkMh9tC85eLZLRpn
# Ваш секретный ключ:
# YCPsjYDacRI4FhSwxlkVVHLdsgKE4zlgOoZYSnUE

class Storage:
    def __init__(self, bucket_name):
        # Название бакета, в котором будут хранится файлы
        # (сделал параметром, чтобы класс был универсальным и можно было использовать разные бакеты и не менять код)
        self.bucket_name = bucket_name
        self.s3 = boto3.client('s3',
                               endpoint_url='https://storage.yandexcloud.net',
                               region_name='ru-central1',
                               aws_access_key_id='YCAJE4Vn2tkMh9tC85eLZLRpn',
                               aws_secret_access_key='YCPsjYDacRI4FhSwxlkVVHLdsgKE4zlgOoZYSnUE'
                               )

    def save_file(self, file_name):
        try:
            # Сохраняем файл
            # первый параметр - файл, который находится локально
            # третий параметр - название файла, которое будет в облаке храниться
            self.s3.upload_file('tmp_files/' + file_name, self.bucket_name, file_name)
            print(self.s3.waiter_names())
        except Exception as e:
            logger.error(f'Возникла ошибка при сохранении файла со стороны Yandex storage\n'
                         f'{e}')
            raise e
        # Формируем ссылку, где лежит(и отдыхает) файл, который только что сохранили
        file_url = f'{self.s3.meta.endpoint_url}/{self.bucket_name}/{file_name}'
        return file_url
