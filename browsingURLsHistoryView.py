import os, json, shutil, sqlite3, datetime
import pandas as pd
from InquirerPy import inquirer
from mylibrary.Style import Clean
from Crypto.Cipher import AES



def get_unique_filename(path, name, extension):
    counter = 0
    file_path = os.path.join(path, f"{name}{extension}")
    while os.path.exists(file_path):
        counter += 1
        file_path = os.path.join(path, f"{name}({counter}){extension}")
    return file_path

def chromium_timestamp_to_datetime(timestamp):
    epoch_start = datetime.datetime(1601, 1, 1)
    return str(epoch_start + datetime.timedelta(microseconds=timestamp))



class GetURLsHistory:
    @staticmethod
    def operaGX():
        visits = []
        db_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera GX Stable\History')
        temp_db = 'temp_opera_gx.db'
        shutil.copyfile(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")
        history = cursor.fetchall()
        for url, title, visit_count, last_visit_time in history:
            visits.append({'browser': "Opera GX", 'title': title, 'url': url, 'visit_count': visit_count, 'last_visit_time': chromium_timestamp_to_datetime(last_visit_time)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return visits

    @staticmethod
    def opera():
        visits = []
        db_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera Stable\History')
        temp_db = 'temp_opera.db'
        shutil.copyfile(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")
        history = cursor.fetchall()
        for url, title, visit_count, last_visit_time in history:
            visits.append({'browser': "Opera", 'title': title, 'url': url, 'visit_count': visit_count, 'last_visit_time': chromium_timestamp_to_datetime(last_visit_time)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return visits
    
    @staticmethod
    def chrome():
        visits = []
        db_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\History')
        temp_db = 'temp_chrome.db'
        shutil.copyfile(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")
        history = cursor.fetchall()
        for url, title, visit_count, last_visit_time in history:
            visits.append({'browser': "Chrome", 'title': title, 'url': url, 'visit_count': visit_count, 'last_visit_time': chromium_timestamp_to_datetime(last_visit_time)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return visits

    @staticmethod
    def edge():
        visits = []
        db_path = os.path.join(os.environ['LOCALAPPDATA'], r'Microsoft\Edge\User Data\Default\History')
        temp_db = 'temp_edge.db'
        shutil.copyfile(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")
        history = cursor.fetchall()
        for url, title, visit_count, last_visit_time in history:
            visits.append({'browser': "Edge", 'title': title, 'url': url, 'visit_count': visit_count, 'last_visit_time': chromium_timestamp_to_datetime(last_visit_time)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return visits

    @staticmethod
    def brave():
        visits = []
        db_path = os.path.join(os.environ['LOCALAPPDATA'], r'BraveSoftware\Brave-Browser\User Data\Default\History')
        temp_db = 'temp_brave.db'
        shutil.copyfile(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")
        history = cursor.fetchall()
        for url, title, visit_count, last_visit_time in history:
            visits.append({'browser': "Brave", 'title': title, 'url': url, 'visit_count': visit_count, 'last_visit_time': chromium_timestamp_to_datetime(last_visit_time)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return visits
    
    @staticmethod
    def vivaldi():
        visits = []
        db_path = os.path.join(os.environ['LOCALAPPDATA'], r'Vivaldi\User Data\Default\History')
        temp_db = 'temp_vivaldi.db'
        shutil.copyfile(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, visit_count, last_visit_time FROM urls")
        history = cursor.fetchall()
        for url, title, visit_count, last_visit_time in history:
            visits.append({'browser': "Vivaldi", 'title': title, 'url': url, 'visit_count': visit_count, 'last_visit_time': chromium_timestamp_to_datetime(last_visit_time)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return visits

    @staticmethod
    def firefox():
        visits = []
        profile_path = os.path.join(os.environ['APPDATA'], r'Mozilla\Firefox\Profiles')
        profile = [p for p in os.listdir(profile_path) if p.endswith('.default-release')][0]
        db_path = os.path.join(profile_path, profile, 'places.sqlite')

        temp_db = 'temp_firefox.db'
        shutil.copyfile(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()

        cursor.execute("SELECT url, title, visit_count, last_visit_date FROM moz_places")
        history = cursor.fetchall()

        for url, title, visit_count, last_visit_date in history:
            last_visit_time = None
            if last_visit_date:
                last_visit_time = str(datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=last_visit_date))

            visits.append({'browser': "Firefox", 'title': title, 'url': url, 'visit_count': visit_count, 'last_visit_time': last_visit_time})

        cursor.close()
        conn.close()
        os.remove(temp_db)

        return visits


class Export:
    @staticmethod
    def database(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "browsingurlshistoryview"
        ext = ".db"
        db_path = get_unique_filename(downloads_path, base_name, ext)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE browsingvisitshistoryview (navegador TEXT, site TEXT, link TEXT, visitas INTEGER, ultima_visita TEXT)")
        conn.commit()

        registros = [(i['browser'], i['title'], i['url'], i['visit_count'], i['last_visit_time']) for i in data]
        cursor.executemany("INSERT INTO browsingvisitshistoryview (navegador, site, link, visitas, ultima_visita) VALUES (?, ?, ?, ?, ?)", registros)

        conn.commit()

        conn.close()
        return db_path
    
    @staticmethod
    def excel(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "browsingvisitshistoryview"
        ext = ".xlsx"
        excel_path = get_unique_filename(downloads_path, base_name, ext)

        df = pd.DataFrame(data)
        df = df.rename(columns={'browser': "navegador", 'title': "site", 'url': "link", 'visit_count': "visitas", 'last_visit_time': "ultima_visita"})
        df.to_excel(excel_path, index=False)

        return excel_path

    @staticmethod
    def json(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "browsingurlshistoryview"
        ext = ".json"
        json_path = get_unique_filename(downloads_path, base_name, ext)

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return json_path



def getURLsHistory():
    while True:
        Clean()
        browsers = inquirer.checkbox(message="Escolha quais navegadores deseja investigar:", choices=["Chrome", "Firefox", "Edge", "Opera", "Opera GX", "Brave", "Vivaldi"],).execute()
        visits = []
        Clean()

        if 'Chrome' in browsers:
            try:
                for i in GetURLsHistory.chrome():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Firefox' in browsers:
            try:
                for i in GetURLsHistory.firefox():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Edge' in browsers:
            try:
                for i in GetURLsHistory.edge():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Opera' in browsers:
            try:
                for i in GetURLsHistory.opera():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Opera GX' in browsers:
            try:
                for i in GetURLsHistory.operaGX():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Brave' in browsers:
            try:
                for i in GetURLsHistory.brave():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Vivaldi' in browsers:
            try:
                for i in GetURLsHistory.vivaldi():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if not browsers:
            pass
        else:
            return visits

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