import time
from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable


class CssSelectorAbstract(ABC):
    def __init__(self, webbot, wait_d, wait_r):
        self.webbot = webbot
        self.wait_d = wait_d
        self.wait_r = wait_r

    def _preencher_input_por_css_selector(self, css_element: str, value: str, rapido=False) -> bool:
        """
        Preenche um campo de entrada identificado pelo seletor CSS.

        Args:
            css_element (str): O seletor CSS do campo de entrada.
            value (str): O valor a ser inserido no campo.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.CSS_SELECTOR, css_element)))
            elemento.clear()
            elemento.send_keys(value)
            return True
        except Exception:
            return False

    def _click_por_css_selector(self, css_element: str, rapido=False) -> bool:
        """
        Clica em um elemento identificado pelo seletor CSS.

        Args:
            css_element (str): O seletor CSS do elemento a ser clicado.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(element_to_be_clickable((By.CSS_SELECTOR, css_element))).click()
            return True
        except Exception:
            return False

    def _existe_css_selector(self, css_element: str) -> bool:
        """
        Verifica se existe pelo menos um elemento com o seletor CSS especificado.

        Args:
            css_element (str): O seletor CSS do elemento a ser verificado.

        Returns:
            bool: True se pelo menos um elemento com o seletor CSS existir, False caso contrário.
        """
        time.sleep(1)
        return len(self.webbot.find_elements(By.CSS_SELECTOR, css_element)) > 0

    def _existe_css_selector_text(self, css_element: str, texto: str) -> bool:
        """
        Verifica se existe pelo menos um elemento com o seletor CSS especificado contendo o texto fornecido.

        Args:
            css_element (str): O seletor CSS do elemento a ser verificado.
            texto (str): O texto a ser verificado nos elementos encontrados.

        Returns:
            bool: True se pelo menos um elemento com o seletor CSS e texto especificado existir, False caso contrário.
        """
        time.sleep(1)
        return self._existe_css_selector(css_element) and texto in [text.text for text in self.webbot.find_elements(By.CSS_SELECTOR, css_element)]

    def _verificar_atributo_por_css_selector(self, css_element: str, atributo: str, valor: str, rapido=False) -> bool:
        """
        Verifica se um atributo de um elemento identificado pelo seletor CSS corresponde ao valor fornecido.

        Args:
            css_element (str): O seletor CSS do elemento.
            atributo (str): O nome do atributo a ser verificado.
            valor (str): O valor esperado do atributo.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se o valor do atributo corresponder, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.CSS_SELECTOR, css_element)))
            return elemento.get_attribute(atributo) == valor
        except Exception:
            return False

    def _obter_texto_por_css_selector(self, css_element: str, rapido=False) -> str:
        """
        Obtém o texto de um elemento identificado pelo seletor CSS.

        Args:
            css_element (str): O seletor CSS do elemento.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            str: O texto do elemento. Se o elemento não for encontrado, retorna uma string vazia.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.CSS_SELECTOR, css_element)))
            return elemento.text
        except Exception:
            return ""

    def _esperar_elemento_visivel_por_css_selector(self, css_element: str, rapido=False) -> bool:
        """
        Espera até que um elemento identificado pelo seletor CSS se torne visível.

        Args:
            css_element (str): O seletor CSS do elemento.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se o elemento se tornar visível, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(lambda driver: driver.find_element(By.CSS_SELECTOR, css_element).is_displayed())
            return True
        except Exception:
            return False

    def _esperar_elemento_invisivel_por_css_selector(self, css_element: str, rapido=False) -> bool:
        """
        Espera até que um elemento identificado pelo seletor CSS se torne invisível.

        Args:
            css_element (str): O seletor CSS do elemento.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se o elemento se tornar invisível, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(lambda driver: not driver.find_element(By.CSS_SELECTOR, css_element).is_displayed())
            return True
        except Exception:
            return False

    def _scroll_para_elemento_por_css_selector(self, css_element: str, rapido=False) -> bool:
        """
        Rola a página até um elemento identificado pelo seletor CSS.

        Args:
            css_element (str): O seletor CSS do elemento.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a rolagem for bem-sucedida, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.CSS_SELECTOR, css_element)))
            self.webbot.execute_script("arguments[0].scrollIntoView();", elemento)
            return True
        except Exception:
            return False

    def _verificar_elemento_ativado_por_css(self, css_element: str) -> bool:
        """
        Verifica se um elemento identificado pelo seletor CSS está ativado.

        Um elemento é considerado ativado se pode ser interagido (clicado, selecionado, etc.).

        Args:
            css_element (str): O seletor CSS do elemento a ser verificado.

        Returns:
            bool: True se o elemento estiver ativado, False caso contrário.
        """
        try:
            return self.webbot.find_element(By.CSS_SELECTOR, css_element).is_enabled()
        except Exception:
            return False

    def _verificar_elemento_selecionado_por_css(self, css_element: str) -> bool:
        """
        Verifica se um elemento identificado pelo seletor CSS está selecionado.

        Um elemento é considerado selecionado se estiver marcado (por exemplo, em um checkbox ou radio button).

        Args:
            css_element (str): O seletor CSS do elemento a ser verificado.

        Returns:
            bool: True se o elemento estiver selecionado, False caso contrário.
        """
        try:
            return self.webbot.find_element(By.CSS_SELECTOR, css_element).is_selected()
        except Exception:
            return False

    def _verificar_texto_contido_por_css(self, css_element: str, texto: str) -> bool:
        """
        Verifica se o texto fornecido está contido no texto de um elemento identificado pelo seletor CSS.

        O método busca o texto dentro do conteúdo do elemento especificado pelo seletor CSS.

        Args:
            css_element (str): O seletor CSS do elemento a ser verificado.
            texto (str): O texto a ser verificado como contido no texto do elemento.

        Returns:
            bool: True se o texto estiver contido, False caso contrário.
        """
        try:
            return texto in self.webbot.find_element(By.CSS_SELECTOR, css_element).text
        except Exception:
            return False
