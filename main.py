import pydantic
from fastapi import FastAPI
import uvicorn
from fastapi import File, UploadFile

from places import save_place_
from service import save_file_in_storage
from pydantic import BaseModel

app = FastAPI()


class Place(BaseModel):
    name: str
    description: str


@app.post('/save_place')
def save_place(place: Place, file: UploadFile = File(...)):
    try:
        file_url = save_file_in_storage(file)
        id = save_place_(place, file_url)
    except Exception:
        return {'error': f'Возникла ошибка при сохранении места'}
    return {'place_id': id}


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
