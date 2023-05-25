import os
import uuid

import pydub


def convert_to_mp3(filepath: str, record_uuid: uuid.UUID) -> str:
    sound = pydub.AudioSegment.from_wav(filepath)
    filename = str(record_uuid) + '.mp3'
    path = os.path.join('src', 'static', filename)  # изменить путь сохранения mp3 файлов
    sound.export(path, format="mp3")
    os.remove(filepath)  # Удалить wav файл после конвертации в mp3
    return path
