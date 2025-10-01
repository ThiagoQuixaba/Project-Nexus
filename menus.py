import webPasswordsView, browsingVisitsHistoryView, browsingURLsHistoryView, photoMetadataView
from InquirerPy import inquirer
from mylibrary.Style import Clean



class Default:
    @staticmethod
    def select():
        Clean()
        return inquirer.select(message="Informe qual serviço deseja executar:", choices=["WebPasswordsView", "BrowsingVisitsHistoryView", "BrowsingURLsHistoryView", "PhotoMetadataView"]).execute()



class WebPasswordsView:
    @staticmethod
    def list():
        Clean()
        passwords = webPasswordsView.getPasswords()
        if passwords != []:
            for i in passwords:
                print(f"{'-' * 3}{'=' * 162}{'-' * 3}")
                print(f"Browser: {i['browser']}\nWebsite: {i['url']}\nUsuario: {i['user']}\nSenha: {i['password']}\nCreated in: {i['created']}\nLast used: {i['lastUsed']}")
            print(f"{'-' * 3}{'=' * 162}{'-' * 3}")
            input()
            WebPasswordsView.export(passwords)
        else:
            input("Nenhuma informação encontrada.")
    
    @staticmethod
    def export(passwords):
        Clean()
        exportar = inquirer.select(message="Deseja exportar essas informações?", choices=['Sim', 'Não'],).execute()
        if exportar == 'Sim':
            webPasswordsView.export(passwords)
        Clean()



class BrowsingVisitsHistoryView:
    @staticmethod
    def getVisits():
        Clean()
        visits = browsingVisitsHistoryView.getVisitsHistory()
        BrowsingVisitsHistoryView.export(visits)
    
    @staticmethod
    def export(visits):
        Clean()
        exportar = inquirer.select(message="Deseja exportar essas informações?", choices=['Sim', 'Não'],).execute()
        if exportar == 'Sim':
            browsingVisitsHistoryView.export(visits)
        Clean()



class BrowsingURLsHistoryView:
    def getURLs():
        Clean()
        URLs = browsingURLsHistoryView.getURLsHistory()
        BrowsingURLsHistoryView.export(URLs)
    
    @staticmethod
    def export(URLs):
        Clean()
        exportar = inquirer.select(message="Deseja exportar essas informações?", choices=['Sim', 'Não'],).execute()
        if exportar == 'Sim':
            browsingURLsHistoryView.export(URLs)
        Clean()



class PhotoMetadataView:
    @staticmethod
    def list():
        Clean()
        metadatas = photoMetadataView.getExif()
        if metadatas:
            print(f"{'-' * 3}{'=' * 177}{'-' * 3}")
            for i in metadatas:
                print(f"{i['tag']}: {i['value']}")
            print(f"{'-' * 3}{'=' * 177}{'-' * 3}")
            input()
            PhotoMetadataView.export(metadatas)
        else:
            input("Nenhuma informação encontrada.")
    
    @staticmethod
    def export(metadatas):
        Clean()
        exportar = inquirer.select(message="Deseja exportar essas informações?", choices=['Sim', 'Não'],).execute()
        if exportar == 'Sim':
            photoMetadataView.export(metadatas)
        Clean()


