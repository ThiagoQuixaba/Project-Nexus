import os, json, shutil, sqlite3, datetime
import pandas as pd
from InquirerPy import inquirer
from mylibrary.Style import Clean




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



class GetVisitsHistory:
    @staticmethod
    def operaGX():
        visits = []
        db_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera GX Stable\History')
        temp_db = 'temp_opera_gx.db'
        shutil.copyfile(db_path, temp_db)

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT url, visit_time, from_visit, visit_duration FROM visits")
        history = cursor.fetchall()
        for url_id, visit_time, from_visit_id, visit_duration in history:
            url = None
            title = None
            if url_id != 0:
                cursor.execute("SELECT url, title FROM urls WHERE id = ?", (url_id,))
                row = cursor.fetchone()
                if row:
                    url, title = row

            from_visit = None
            if from_visit_id != 0:
                cursor.execute("SELECT url FROM urls WHERE id = ?", (from_visit_id,))
                visit_rows = cursor.fetchone()
                from_visit = visit_rows[0] if visit_rows else None

            visits.append({'browser': "Opera GX", 'site': title, 'url': url, 'visitTime': chromium_timestamp_to_datetime(visit_time), 'fromVisit': from_visit, 'visitDuration': str(datetime.timedelta(microseconds=visit_duration))})

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
        cursor.execute("SELECT url, visit_time, from_visit, visit_duration FROM visits")
        history = cursor.fetchall()
        for url_id, visit_time, from_visit_id, visit_duration in history:
            url = None
            title = None
            if url_id != 0:
                cursor.execute("SELECT url, title FROM urls WHERE id = ?", (url_id,))
                row = cursor.fetchone()
                if row:
                    url, title = row

            from_visit = None
            if from_visit_id != 0:
                cursor.execute("SELECT url FROM urls WHERE id = ?", (from_visit_id,))
                visit_rows = cursor.fetchone()
                from_visit = visit_rows[0] if visit_rows else None

            visits.append({'browser': "Opera", 'site': title, 'url': url, 'visitTime': chromium_timestamp_to_datetime(visit_time), 'fromVisit': from_visit, 'visitDuration': str(datetime.timedelta(microseconds=visit_duration))})

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
        cursor.execute("SELECT url, visit_time, from_visit, visit_duration FROM visits")
        history = cursor.fetchall()
        for url_id, visit_time, from_visit_id, visit_duration in history:
            url = None
            title = None
            if url_id != 0:
                cursor.execute("SELECT url, title FROM urls WHERE id = ?", (url_id,))
                row = cursor.fetchone()
                if row:
                    url, title = row

            from_visit = None
            if from_visit_id != 0:
                cursor.execute("SELECT url FROM urls WHERE id = ?", (from_visit_id,))
                visit_rows = cursor.fetchone()
                from_visit = visit_rows[0] if visit_rows else None

            visits.append({'browser': "Chrome", 'site': title, 'url': url, 'visitTime': chromium_timestamp_to_datetime(visit_time), 'fromVisit': from_visit, 'visitDuration': str(datetime.timedelta(microseconds=visit_duration))})

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
        cursor.execute("SELECT url, visit_time, from_visit, visit_duration FROM visits")
        history = cursor.fetchall()
        for url_id, visit_time, from_visit_id, visit_duration in history:
            url = None
            title = None
            if url_id != 0:
                cursor.execute("SELECT url, title FROM urls WHERE id = ?", (url_id,))
                row = cursor.fetchone()
                if row:
                    url, title = row

            from_visit = None
            if from_visit_id != 0:
                cursor.execute("SELECT url FROM urls WHERE id = ?", (from_visit_id,))
                visit_rows = cursor.fetchone()
                from_visit = visit_rows[0] if visit_rows else None

            visits.append({'browser': "Edge", 'site': title, 'url': url, 'visitTime': chromium_timestamp_to_datetime(visit_time), 'fromVisit': from_visit, 'visitDuration': str(datetime.timedelta(microseconds=visit_duration))})

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
        cursor.execute("SELECT url, visit_time, from_visit, visit_duration FROM visits")
        history = cursor.fetchall()
        for url_id, visit_time, from_visit_id, visit_duration in history:
            url = None
            title = None
            if url_id != 0:
                cursor.execute("SELECT url, title FROM urls WHERE id = ?", (url_id,))
                row = cursor.fetchone()
                if row:
                    url, title = row

            from_visit = None
            if from_visit_id != 0:
                cursor.execute("SELECT url FROM urls WHERE id = ?", (from_visit_id,))
                visit_rows = cursor.fetchone()
                from_visit = visit_rows[0] if visit_rows else None

            visits.append({'browser': "Brave", 'site': title, 'url': url, 'visitTime': chromium_timestamp_to_datetime(visit_time), 'fromVisit': from_visit, 'visitDuration': str(datetime.timedelta(microseconds=visit_duration))})

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
        cursor.execute("SELECT url, visit_time, from_visit, visit_duration FROM visits")
        history = cursor.fetchall()
        for url_id, visit_time, from_visit_id, visit_duration in history:
            url = None
            title = None
            if url_id != 0:
                cursor.execute("SELECT url, title FROM urls WHERE id = ?", (url_id,))
                row = cursor.fetchone()
                if row:
                    url, title = row

            from_visit = None
            if from_visit_id != 0:
                cursor.execute("SELECT url FROM urls WHERE id = ?", (from_visit_id,))
                visit_rows = cursor.fetchone()
                from_visit = visit_rows[0] if visit_rows else None

            visits.append({'browser': "Vivaldi", 'site': title, 'url': url, 'visitTime': chromium_timestamp_to_datetime(visit_time), 'fromVisit': from_visit, 'visitDuration': str(datetime.timedelta(microseconds=visit_duration))})

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

        cursor.execute("SELECT moz_places.url, moz_places.title, moz_historyvisits.visit_date, moz_historyvisits.from_visit FROM moz_historyvisits JOIN moz_places ON moz_historyvisits.place_id = moz_places.id")
        history = cursor.fetchall()

        for url, title, visit_time, from_visit_id in history:
            visit_dt = str(datetime.datetime(1970, 1, 1) + datetime.timedelta(microseconds=visit_time))

            from_visit = None
            if from_visit_id != 0:
                cursor.execute("SELECT moz_places.url FROM moz_historyvisits JOIN moz_places ON moz_historyvisits.place_id = moz_places.id WHERE moz_historyvisits.id = ?", (from_visit_id,))
                row = cursor.fetchone()
                from_visit = row[0] if row else None

            visits.append({'browser': "Firefox", 'site': title, 'url': url, 'visitTime': visit_dt, 'fromVisit': from_visit, 'visitDuration': None})

        cursor.close()
        conn.close()
        os.remove(temp_db)

        return visits



class Export:
    @staticmethod
    def database(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "browsingvisitshistoryview"
        ext = ".db"
        db_path = get_unique_filename(downloads_path, base_name, ext)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("CREATE TABLE browsingvisitshistoryview (navegador TEXT, site TEXT, link TEXT, data_de_visita TEXT, origem TEXT, duracao_de_visita TEXT)")
        conn.commit()

        registros = [(i['browser'], i['site'], i['url'], i['visitTime'], i['fromVisit'], i['visitDuration']) for i in data]
        cursor.executemany("INSERT INTO browsingvisitshistoryview (navegador, site, link, data_de_visita, origem, duracao_de_visita) VALUES (?, ?, ?, ?, ?, ?)", registros)

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
        df = df.rename(columns={'browser': "navegador", 'site': "site", 'url': "link", 'visitTime': "data_de_visita", 'fromVisit': "origem", 'visitDuration': "duracao_de_visita"})
        df.to_excel(excel_path, index=False)

        return excel_path

    @staticmethod
    def json(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "browsingvisitshistoryview"
        ext = ".json"
        json_path = get_unique_filename(downloads_path, base_name, ext)

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return json_path



def getVisitsHistory():
    while True:
        Clean()
        browsers = inquirer.checkbox(message="Escolha quais navegadores deseja investigar:", choices=["Chrome", "Firefox", "Edge", "Opera", "Opera GX", "Brave", "Vivaldi"],).execute()
        visits = []
        Clean()

        if 'Chrome' in browsers:
            try:
                for i in GetVisitsHistory.chrome():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Firefox' in browsers:
            try:
                for i in GetVisitsHistory.firefox():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Edge' in browsers:
            try:
                for i in GetVisitsHistory.edge():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Opera' in browsers:
            try:
                for i in GetVisitsHistory.opera():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Opera GX' in browsers:
            try:
                for i in GetVisitsHistory.operaGX():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Brave' in browsers:
            try:
                for i in GetVisitsHistory.brave():
                    visits.append(i)
            except FileNotFoundError:
                pass
        if 'Vivaldi' in browsers:
            try:
                for i in GetVisitsHistory.vivaldi():
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