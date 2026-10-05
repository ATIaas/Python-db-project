# Consolidates the database by removing duplicates and delete orders
# Rewrites the file with only the latest valid entries
def consolidate(FILE):
    """
    Elimina duplicados y ordenes de eliminacion del archivo
    Mantiene solo la ultima version valida de cada clave
    """
    seen_keys = {}

    # Lee el archivo y mantiene el registro más reciente de cada clave
    with open(FILE, 'r') as file:
        for line in file:
            line = line.rstrip("\n")
            if not line:
                continue

            if line[0] == '?':
                # Es una orden de eliminacion
                key = line.lstrip("?")
                seen_keys[key] = None  # None indica que fue eliminado
            else:
                # Es un par key:data
                if ':' in line:
                    key, data = line.split(":", 1)
                    seen_keys[key] = data

    # Reescribe el archivo con solo las entradas validas (no eliminadas)
    with open(FILE, 'w') as file:
        for key, data in seen_keys.items():
            if data is not None:  # Solo escribe si no fue eliminado
                file.write(key + ":" + data + "\n")

    # Recarga los datos en memoria
    getdata()
    return "Database consolidated: " + str(len([v for v in seen_keys.values() if v is not None])) + " valid entries"