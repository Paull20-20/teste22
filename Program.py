from playwright.sync_api import sync_playwright
from time import sleep
import pathlib
import os

class Program:
    with sync_playwright() as p:
        userDataDir = './cache'
        browser = p.firefox.launch_persistent_context(headless=False, user_data_dir=userDataDir)
        page = browser.new_page()

        login_page = page.goto("https://drive.google.com/drive/folders/1zpJPcb4HuS5J5AHSMpMTF1sZLrFA0TFN")

        #Espera o elemento ficar visivel
        def waitElement(self, el):
            status = True
            while status:
                el = self.page.locator(el)
                if el != None and el.is_visible():
                    status = False
        
        # Validação para saber se a aplicação está logada
        if page.locator('text=Fazer login').count() > 0:
            
            # Clicar em Fazer login
            page.locator("text=Fazer login").click(delay=0.5)

            # Digitar o e-mail
            page.fill('//*[@id="identifierId"]', 'sistema@montenegrocontabilidade.com.br')
            page.locator('//*[@id="identifierNext"]/div/button/div[3]').click(delay=0.5)

            # Digitar a senha
            page.fill('#password > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > input:nth-child(1)', 'Monte@labs3094')
            page.locator('#passwordNext button:has-text("Próxima")').click(delay=0.5)
            sleep(1)

        # Validação para saber se há a pasta referente existe
        sleep(1)
        folder_name = 'pastaTeste'
        if page.locator('.Q5txwe').locator(f'text={folder_name}').count() == 0:
            page.keyboard.press('c')
            sleep(1)
            page.keyboard.press('Enter')
            sleep(1)
            page.keyboard.type(f'{folder_name}')
            sleep(1)
            page.keyboard.press('Enter')
            sleep(3)
        
        # Entrar na pasta teste
        sleep(1)
       
        page.locator('.Q5txwe').locator(f'text={folder_name}').dblclick()

        #verificando a quantidade de arquivos dentro da pasta que terá os arquivos a serem enviados para o drive.
        numberFile = 0
        for path in pathlib.Path(f'/home/tiago.oliveira/Área de Trabalho/teste_upload/').iterdir():
            if path.is_file():
                numberFile += 1

        print('\nQuantidade de arquivos dentro do diretório: ', numberFile)


        print('\n*************---------------***************')

        ano = 2020
        for i in range(0, numberFile): #verificando se existe tal arquivo dentro do diretório, retorna true ou false
            file = os.path.exists(rf'/home/tiago.oliveira/Área de Trabalho/teste_upload/{ano}teste.pdf')
            print(file)
            ano = ano + 1


        # Checar quais arquivos existem na pasta e fazer o upload
        for diretorio, subpastas, arquivos in os.walk(r'/home/tiago.oliveira/Área de Trabalho/teste_upload/'):
            sleep(1)
            for arquivo in arquivos:
                #Upload do(s) arquivo(s)
                if page.locator('.Q5txwe').locator(f'text={os.path.join(arquivo)}').count() == 0:
                    with page.expect_file_chooser() as fc_info:
                        page.keyboard.press('c')
                        sleep(1)
                        page.locator('text=Upload de Arquivo').click()
                    file_chooser = fc_info.value
                    file_chooser.set_files(os.path.join(os.path.realpath(diretorio), arquivo))
                    sleep(1)
                else:
                    print(f'o arquivo {os.path.join(arquivo)} ja existe na pasta!')



        while True:
            pass 