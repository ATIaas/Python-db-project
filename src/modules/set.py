from .log_line import set_line
from .validate import validate_key, validate_data

# Saves data under the key's position (overwrites if something was already there)
# Both creates an entry in .txt and in memory
# Raises ValueError if key or data would corrupt the log
def set(key: str, data: str, dataset: dict[str, str], path: str) -> str:
    validate_key(key)
    validate_data(data)

    if key in dataset:
        if dataset[key] == data:
            return "Already exists"

    #Write to log and update dataset
    with open(path, 'a') as file:
        file.write(set_line(key, data))
    dataset[key] = data
    return "saved " + "\"" + data + "\"" + " in key:" + key