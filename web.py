import os
import sys
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

class WebAuto:

    """ 
    Inicializa o webdriver do chrome

    :Args:
        - startingPage : url que vai abrir após abertura da janela do browser
    """
    def __init__(self, driverFolder:str, startingPage:str = ""):
        self.web = webdriver.Chrome(executable_path= self.get_driver_path(driverFolder) )

        if startingPage:
            self.web.get(startingPage)

    def get_driver_path(self, driverFolder):
        """
        Obtem a caminho correto do driver chrome baseado no sistema operativo.
        O mesmo tem de estar na pasta drivers junto ao ficheiro do script, caso contrário irá encerrar o script

        :Returns: 
            Obtem o caminho absoluto do ficheiro do driver chrome ou encerra o script
        """

        driver_folder = str(os.path.dirname(os.path.abspath(__file__))) + driverFolder

        if sys.platform == "linux" or sys.platform == "linux2":
            return  driver_folder + "chrome_linux"
        elif sys.platform == "win32":
            return  driver_folder + "chrome_windows.exe"
        elif sys.platform == "darwin":
            return  driver_folder + "chrome_mac"
        else:
            print("Sistema Operativo não suportado")
            sys.exit()

    
    def get_window_title(self):
        """
        Obter o título da janela atual

        :Returns:
            Título da janela do browser. Caso a mesma não exista retorna string vazia

        :Exceptions:
            NoSuchWindowException caso o browser tenha sido fechado
        """
        try:
            self.web.title
        except NoSuchWindowException:
            return False

        return True
    
    def does_element_exist(self, element_id:str = "", element_class:str = ""):
        """
        Verifica se elemento exista na página atual do browser

        :Args:
            element_id: id do elemento a ser localizado
            element_class: class do elemento a ser localizado

        :Returns:
            True se elemento existir, falso caso contrário

        Exceptions:
            NoSuchElementException caso o elemento não exista
        """
        try:
            if element_id:
                self.web.find_element_by_id(element_id)
            elif element_class:
                self.web.find_element_by_class_name(element_class)
            else:
                return False

        except NoSuchElementException:
            return False

        return True

    def get_elements(self, element_class:str = ""):
        """
        Obter elementos web que contenham a class

        :Args:
            element_class: class do elemento web

        :Returns:
            Lista de elementos se encotrado algum caso contrário retorna False

        """
        try:
            if element_class:
                return self.web.find_elements_by_class_name(element_class)
            else:
                return False

        except NoSuchElementException:
            return False

    def get_element_attribute(self, element, attribute:str = ""):
        """
        Obter atributo do elemento web

        :Args:
            element : elemento web
            attribute: atributo que vai procurar

        :Returns:
            Atributo se encontrar ou False se não existir

        """
        try:
            if attribute:
                return element.get_attribute(attribute)
            else:
                return False
        except StaleElementReferenceException:
            return False

    def close(self):
        """
        Destroi o webdriver
        """
        self.web.close()
