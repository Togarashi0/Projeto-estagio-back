import time
from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import element_to_be_clickable


class ClassNameAbstract(ABC):
    def __init__(self, webbot, wait_d, wait_r):
        self.webbot = webbot
        self.wait_d = wait_d
        self.wait_r = wait_r

    def _click_por_class(self, class_element: str, rapido=False) -> bool:
        """
        Clica em um elemento identificado pelo nome da classe.

        Args:
            class_element (str): O nome da classe do elemento a ser clicado.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(element_to_be_clickable((By.CLASS_NAME, class_element))).click()
            return True
        except Exception:
            return False

    def _existe_class_por_id(self, id_element: str, class_html: str) -> bool:
        """
        Verifica se um elemento identificado pelo ID possui uma determinada classe.

        Args:
            id_element (str): O ID do elemento.
            class_html (str): A classe HTML a ser verificada.

        Returns:
            bool: True se a classe existir no elemento, False caso contrário.
        """
        time.sleep(1)
        return class_html in self.webbot.find_element(By.ID, id_element).get_attribute("class")

    def _verificar_texto_por_class(self, class_element: str, texto: str) -> bool:
        """
        Verifica se um elemento identificado pelo nome da classe contém o texto fornecido.

        Args:
            class_element (str): O nome da classe do elemento.
            texto (str): O texto a ser verificado nos elementos encontrados.

        Returns:
            bool: True se o texto for encontrado, False caso contrário.
        """
        time.sleep(1)
        elementos = self.webbot.find_elements(By.CLASS_NAME, class_element)
        return any(texto in elemento.text for elemento in elementos)

    def _obter_texto_por_class(self, class_element: str) -> str:
        """
        Obtém o texto de um elemento identificado pelo nome da classe.

        Args:
            class_element (str): O nome da classe do elemento.

        Returns:
            str: O texto do elemento. Se o elemento não for encontrado, retorna uma string vazia.
        """
        try:
            elemento = (self.wait_d).until(lambda driver: driver.find_element(By.CLASS_NAME, class_element))
            return elemento.text
        except Exception:
            return ""

    def _esperar_elemento_visivel_por_class(self, class_element: str) -> bool:
        """
        Espera até que um elemento identificado pelo nome da classe se torne visível.

        Args:
            class_element (str): O nome da classe do elemento.

        Returns:
            bool: True se o elemento se tornar visível, False caso contrário.
        """
        try:
            self.wait_d.until(lambda driver: driver.find_element(By.CLASS_NAME, class_element).is_displayed())
            return True
        except Exception:
            return False

    def _esperar_elemento_invisivel_por_class(self, class_element: str) -> bool:
        """
        Espera até que um elemento identificado pelo nome da classe se torne invisível.

        Args:
            class_element (str): O nome da classe do elemento.

        Returns:
            bool: True se o elemento se tornar invisível, False caso contrário.
        """
        try:
            self.wait_d.until(lambda driver: not driver.find_element(By.CLASS_NAME, class_element).is_displayed())
            return True
        except Exception:
            return False

    def _verificar_atributo_por_class(self, class_element: str, atributo: str, valor: str) -> bool:
        """
        Verifica se um atributo de um elemento identificado pelo nome da classe corresponde ao valor fornecido.

        Args:
            class_element (str): O nome da classe do elemento.
            atributo (str): O nome do atributo a ser verificado.
            valor (str): O valor esperado do atributo.

        Returns:
            bool: True se o valor do atributo corresponder, False caso contrário.
        """
        try:
            elemento = self.wait_d.until(lambda driver: driver.find_element(By.CLASS_NAME, class_element))
            return elemento.get_attribute(atributo) == valor
        except Exception:
            return False

    def _scroll_para_elemento_por_class(self, class_element: str) -> bool:
        """
        Rola a página até um elemento identificado pelo nome da classe.

        Args:
            class_element (str): O nome da classe do elemento.

        Returns:
            bool: True se a rolagem for bem-sucedida, False caso contrário.
        """
        try:
            elemento = self.wait_d.until(lambda driver: driver.find_element(By.CLASS_NAME, class_element))
            self.webbot.execute_script("arguments[0].scrollIntoView();", elemento)
            return True
        except Exception:
            return False

    def _verificar_elemento_ativado_por_class(self, class_element: str) -> bool:
        """
        Verifica se um elemento identificado pelo nome da classe está ativado.

        Um elemento é considerado ativado se pode ser interagido (clicado, selecionado, etc.).

        Args:
            class_element (str): O nome da classe do elemento a ser verificado.

        Returns:
            bool: True se o elemento estiver ativado, False caso contrário.
        """
        try:
            return self.webbot.find_element(By.CLASS_NAME, class_element).is_enabled()
        except Exception:
            return False

    def _verificar_elemento_selecionado_por_class(self, class_element: str) -> bool:
        """
        Verifica se um elemento identificado pelo nome da classe está selecionado.

        Um elemento é considerado selecionado se estiver marcado (por exemplo, em um checkbox ou radio button).

        Args:
            class_element (str): O nome da classe do elemento a ser verificado.

        Returns:
            bool: True se o elemento estiver selecionado, False caso contrário.
        """
        try:
            return self.webbot.find_element(By.CLASS_NAME, class_element).is_selected()
        except Exception:
            return False

    def _verificar_texto_contido_por_class(self, class_element: str, texto: str) -> bool:
        """
        Verifica se o texto fornecido está contido no texto de um elemento identificado pelo nome da classe.

        O método busca o texto dentro do conteúdo do elemento especificado pelo nome da classe.

        Args:
            class_element (str): O nome da classe do elemento a ser verificado.
            texto (str): O texto a ser verificado como contido no texto do elemento.

        Returns:
            bool: True se o texto estiver contido, False caso contrário.
        """
        try:
            return texto in self.webbot.find_element(By.CLASS_NAME, class_element).text
        except Exception:
            return False
