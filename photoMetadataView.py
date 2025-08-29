import os, sqlite3, json
import pandas as pd
from InquirerPy import inquirer
from mylibrary.Style import Clean
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS



def get_unique_filename(path, name, extension):
    counter = 0
    file_path = os.path.join(path, f"{name}{extension}")
    while os.path.exists(file_path):
        counter += 1
        file_path = os.path.join(path, f"{name}({counter}){extension}")
    return file_path



class Exif:
    @staticmethod
    def get(file):
        image = Image.open(file)
        exif_data = image._getexif()
        if not exif_data:
            return None
        exif = []
        for tag, value in exif_data.items():
            decoded = TAGS.get(tag, tag)
            exif.append({'tag': decoded, 'value': value})
        return exif

    @staticmethod
    def get_GPS(exif: list[dict]):
        if not exif or not any(i['tag'] == "GPSInfo" for i in exif):
            pass
        else:
            gps_info = next(i['value'] for i in exif if i['tag'] == "GPSInfo")

            gps_data = {}
            for key in gps_info.keys():
                decode = GPSTAGS.get(key, key)
                gps_data[decode] = gps_info[key]

            

            exif.append({'tag': "Latitude", 'value': Exif.convert_GPS(gps_data["GPSLatitude"], gps_data["GPSLatitudeRef"])})
            exif.append({'tag': "Longitude", 'value': Exif.convert_GPS(gps_data["GPSLongitude"], gps_data["GPSLongitudeRef"])})
    
    @staticmethod
    def convert_GPS(coord, ref):
        deg, min, sec = coord
        deg, min, sec = float(deg), float(min), float(sec)
        dec = deg + min / 60 + sec / 3600
        if ref in ["S", "W"]:
            dec = -dec
        return dec



class Export:
    @staticmethod
    def database(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "photovetadataview"
        ext = ".db"
        db_path = get_unique_filename(downloads_path, base_name, ext)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE photovetadataview (tag TEXT, value TEXT)")
        conn.commit()

        registros = [(str(i['tag']), str(i['value'])) for i in data]
        cursor.executemany("INSERT INTO photovetadataview (tag, value) VALUES (?, ?)", registros)

        conn.commit()

        conn.close()
        return db_path

    @staticmethod
    def excel(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "photovetadataview"
        ext = ".xlsx"
        excel_path = get_unique_filename(downloads_path, base_name, ext)

        df = pd.DataFrame(data)
        df.to_excel(excel_path, index=False)

        return excel_path

    @staticmethod
    def json(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "photovetadataview"
        ext = ".json"
        json_path = get_unique_filename(downloads_path, base_name, ext)

        def default_serializer(obj):
            if isinstance(obj, bytes):
                return obj.hex()  
            return str(obj)

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=default_serializer)

        return json_path



def getExif():
    Clean()
    foto = input("Digite o caminho da foto que deseja investigar metadados: ")
    if os.path.isfile(foto):
        fotoExif = Exif.get(foto)
        Exif.get_GPS(fotoExif)

        return fotoExif
    else:
        print(f'"{foto}" não é um arquivo valido.')

def export(data: list[dict]):
    Clean()
    choices = inquirer.checkbox(message="Escolha para quais tipos de arquivo deseja exportar:", choices=[".db", ".xlsx", ".json"],).execute()
    Clean()

    if '.db' in choices:
        print(f'{Export.database(data)}')
    if '.xlsx' in choices:
        print(f'{Export.excel(data)}')
    if '.json' in choices:
        print(f'{Export.json(data)}')

    input()
    Clean()