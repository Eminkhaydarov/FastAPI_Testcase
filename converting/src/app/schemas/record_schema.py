from pydantic import BaseModel, AnyUrl


class UploadSchema(BaseModel):
    download_link: AnyUrl
