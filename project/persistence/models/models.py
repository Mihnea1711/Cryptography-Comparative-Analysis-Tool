import json

from utils.constants import METADATA_FILE_ID


class Metadata:
    def __init__(self, file_id=None):
        self.file_id = file_id

    def __dict__(self):  # Corrected
        return {
            METADATA_FILE_ID: self.file_id,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def to_json(self):
        return json.dumps(self.__dict__())

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls.from_dict(data)

    def __str__(self):
        return f"Metadata(file_id={self.file_id})"

