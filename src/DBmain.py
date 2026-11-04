from src.modules import consolidate
from src.modules import initialize
from src.modules import get
from src.modules import set
from src.modules import delete

class Database:
    def __init__(self, path = "./data"):
        self.dataset = initialize.start_dataset(path)
        self.path = path

    def set(self, key, value):
        try:
            set.set(key, value, self.dataset, self.path)
            return {"ok": True, "Result": "Set key " + key + " to " + value}
        except:
            return {"ok": False, "Result": "Integrate this with the exceptions later"}

    def get(self, key):
        try:
            res = get.get(key, self.dataset)
            return {"ok": True, "Result": res}
        except:
            return {"ok": False, "Result": "Integrate this with the exceptions later"}

    def delete(self, key):
        try:
            delete.delete(key, self.dataset, self.path)
            return {"ok": True, "Result": "Deleted key " + key}
        except:
            return {"ok": False, "Result": "Integrate this with the exceptions later"}

    def consolidate(self):
        try:
            consolidate.consolidate(self.path, self.dataset)
            return {"ok": True, "Result": "Consolidated"}
        except:
            return {"ok": False, "Result": "Integrate this with the exceptions later"}


defpath = "./data"
db = Database(defpath)
print(db.set("donkey", "kong"))
print(db.get("donkey"))
print(db.delete("donkey"))
#print(db.consolidate())