import json
from datetime import date, timedelta


class JsonFile:

    def __init__(self, path):
        self.path = path

    def read(self):
        with open(self.path, "r") as f:
            data = json.load(f)
        return data

    def write(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)


class DateTime:

    def yesterday():
        return date.today() - timedelta(days=1)

    def yyyymmdd(date):
        # YYYY-MM-DD
        return date.strftime("%Y-%m-%d")
