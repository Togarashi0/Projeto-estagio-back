import time
from abc import ABC

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_element_located, element_to_be_clickable


class IdAbstract(ABC):
    def __init__(self, webbot, wait_d, wait_r):
        self.webbot = webbot
        self.wait_d = wait_d
        self.wait_r = wait_r

    def _selecionar_option_por_id_visible_text_js(self, id_element: str, value_element: str, rapido=False) -> bool:
        """
        Seleciona uma opção de um elemento <select> pelo seu ID usando JavaScript, baseado no texto visível da opção.

        Args:
            id_element (str): O ID do elemento <select>.
            value_element (str): O texto visível da opção a ser selecionada.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            select_element = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.ID, id_element)))
            self.webbot.execute_script("arguments[0].style.display = 'block';", select_element)
            self.webbot.execute_script(f"document.getElementById('{id_element}').value = '{value_element}';")
            return True
        except Exception:
            return False

    def _selecionar_valor_por_id(self, id_element: str, value_element: str, rapido=False) -> bool:
        """
        Seleciona uma opção de um elemento <select> pelo seu ID, baseado no valor da opção.

        Args:
            id_element (str): O ID do elemento <select>.
            value_element (str): O valor da opção a ser selecionada.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.ID, id_element))).select_by_value(value_element)
            return True
        except Exception:
            return False

    def _selecionar_visible_text_por_id(self, id_element: str, value_element: str, rapido: bool = False) -> bool:
        """
        Seleciona uma opção de um elemento <select> pelo seu ID, baseado no texto visível da opção.

        Args:
            id_element (str): O ID do elemento <select>.
            value_element (str): O texto visível da opção a ser selecionada.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.ID, id_element))).select_by_visible_text(value_element)
            return True
        except Exception:
            return False

    def _selecionar_option_por_id_visible_text(self, id_element: str, value_element: str, rapido: bool = False) -> bool:
        """
        Seleciona uma opção de um elemento <select> pelo seu ID, baseado no texto visível da opção.

        Args:
            id_element (str): O ID do elemento <select>.
            value_element (str): O texto visível da opção a ser selecionada.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.ID, id_element))).select_by_visible_text(value_element)
            return True
        except Exception:
            return False

    def _selecionar_option_por_id_visible_text_loop(self, id_element: str, value_element: str):
        """
        Seleciona uma opção de um elemento <select> pelo seu ID, baseado no texto visível da opção,
        com tentativas repetidas.

        Args:
            id_element (str): O ID do elemento <select>.
            value_element (str): O texto visível da opção a ser selecionada.

        Raises:
            RuntimeError: Se a opção não puder ser selecionada após 20 tentativas.
        """
        i = 0
        while True:
            try:
                self._selecionar_option_por_id_visible_text(id_element, value_element)
                break
            except Exception as e:
                if i > 19:
                    raise RuntimeError(f"Erro ao tentar selecionar a ação: {e}")
                i += 1
                time.sleep(1)

    def _preencher_input_por_id(self, id_element: str, value: str, rapido=False) -> bool:
        """
        Preenche um campo de entrada identificado pelo ID.

        Args:
            id_element (str): O ID do campo de entrada.
            value (str): O valor a ser inserido no campo.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.ID, id_element)))
            elemento.clear()
            elemento.send_keys(value)
            return True
        except Exception:
            return False

    def _preencher_input_por_id_enter(self, id_element: str, value: str, rapido=False) -> bool:
        """
        Preenche um campo de entrada identificado pelo ID e pressiona Enter.

        Args:
            id_element (str): O ID do campo de entrada.
            value (str): O valor a ser inserido no campo.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.ID, id_element)))
            elemento.clear()
            elemento.send_keys(value)
            elemento.send_keys(Keys.RETURN)
            return True
        except Exception:
            return False

    def _remover_atributo_de_um_elemento_por_id(self, id_element: str, atributo: str, rapido=False) -> bool:
        """
        Remove um atributo de um elemento identificado pelo ID.

        Args:
            id_element (str): O ID do elemento.
            atributo (str): O nome do atributo a ser removido.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            elemento = (self.wait_r if rapido else self.wait_d).until(presence_of_element_located((By.ID, id_element)))
            self.webbot.execute_script(f"arguments[0].removeAttribute('{atributo}')", elemento)
            return True
        except Exception:
            return False

    def _click_por_id(self, id_element: str, rapido=False) -> bool:
        """
        Clica em um elemento identificado pelo ID.

        Args:
            id_element (str): O ID do elemento a ser clicado.
            rapido (bool, optional): Indica se a espera deve ser rápida ou padrão. Default é False.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            (self.wait_r if rapido else self.wait_d).until(element_to_be_clickable((By.ID, id_element))).click()
            return True
        except Exception:
            return False

    def _click_por_id_js(self, id_element: str) -> bool:
        """
        Clica em um elemento identificado pelo ID usando JavaScript.

        Args:
            id_element (str): O ID do elemento a ser clicado.

        Returns:
            bool: True se a operação for bem-sucedida, False caso contrário.
        """
        try:
            self.webbot.execute_script(f"document.getElementById('{id_element}').click()")
            return True
        except Exception:
            return False

    def _existe_id(self, id_element: str) -> bool:
        """
        Verifica se existe pelo menos um elemento com o ID especificado.

        Args:
            id_element (str): O ID do elemento a ser verificado.

        Returns:
            bool: True se pelo menos um elemento com o ID existir, False caso contrário.
        """
        time.sleep(1)
        return len(self.webbot.find_elements(By.ID, id_element)) > 0

    def _verificar_texto_por_id(self, id_element: str, text: str) -> bool:
        """
        Verifica se o texto de um elemento identificado pelo ID corresponde ao texto fornecido.

        Args:
            id_element (str): O ID do elemento.
            text (str): O texto a ser verificado.

        Returns:
            bool: True se o texto corresponder, False caso contrário.
        """
        time.sleep(1)
        return self.webbot.find_element(By.ID, id_element).text.upper() == text.upper()

    def _verificar_atributo_por_id(self, id_element: str, atributo: str, valor: str) -> bool:
        """
        Verifica se um atributo de um elemento identificado pelo ID corresponde ao valor fornecido.

        Args:
            id_element (str): O ID do elemento.
            atributo (str): O nome do atributo a ser verificado.
            valor (str): O valor esperado do atributo.

        Returns:
            bool: True se o valor do atributo corresponder, False caso contrário.
        """
        try:
            elemento = self.wait_d.until(presence_of_element_located((By.ID, id_element)))
            return elemento.get_attribute(atributo) == valor
        except Exception:
            return False

    def _obter_texto_por_id(self, id_element: str) -> str:
        """
        Obtém o texto de um elemento identificado pelo ID.

        Args:
            id_element (str): O ID do elemento.

        Returns:
            str: O texto do elemento. Se o elemento não for encontrado, retorna uma string vazia.
        """
        try:
            elemento = self.wait_d.until(presence_of_element_located((By.ID, id_element)))
            return elemento.text
        except Exception:
            return ""

    def _esperar_elemento_visivel_por_id(self, id_element: str) -> bool:
        """
        Espera até que um elemento identificado pelo ID se torne visível.

        Args:
            id_element (str): O ID do elemento.

        Returns:
            bool: True se o elemento se tornar visível, False caso contrário.
        """
        try:
            self.wait_d.until(lambda driver: driver.find_element(By.ID, id_element).is_displayed())
            return True
        except Exception:
            return False

    def _esperar_elemento_invisivel_por_id(self, id_element: str) -> bool:
        """
        Espera até que um elemento identificado pelo ID se torne invisível.

        Args:
            id_element (str): O ID do elemento.

        Returns:
            bool: True se o elemento se tornar invisível, False caso contrário.
        """
        try:
            self.wait_d.until(lambda driver: not driver.find_element(By.ID, id_element).is_displayed())
            return True
        except Exception:
            return False

    def _scroll_para_elemento_por_id(self, id_element: str) -> bool:
        """
        Rola a página até um elemento identificado pelo ID.

        Args:
            id_element (str): O ID do elemento.

        Returns:
            bool: True se a rolagem for bem-sucedida, False caso contrário.
        """
        try:
            elemento = self.wait_d.until(presence_of_element_located((By.ID, id_element)))
            self.webbot.execute_script("arguments[0].scrollIntoView();", elemento)
            return True
        except Exception:
            return False

    def _verificar_elemento_ativado_por_id(self, id_element: str) -> bool:
        """
        Verifica se um elemento identificado pelo ID está ativado (habilitado para interação).

        Args:
            id_element (str): O ID do elemento.

        Returns:
            bool: True se o elemento estiver ativado, False caso contrário.
        """
        try:
            elemento = self.wait_d.until(presence_of_element_located((By.ID, id_element)))
            return elemento.is_enabled()
        except Exception:
            return False

    def _verificar_elemento_selecionado_por_id(self, id_element: str) -> bool:
        """
        Verifica se um elemento identificado pelo ID está selecionado (aplica-se a elementos de seleção).

        Args:
            id_element (str): O ID do elemento.

        Returns:
            bool: True se o elemento estiver selecionado, False caso contrário.
        """
        try:
            elemento = self.wait_d.until(presence_of_element_located((By.ID, id_element)))
            return elemento.is_selected()
        except Exception:
            return False

    def _verificar_texto_contido_por_id(self, id_element: str, texto: str) -> bool:
        """
        Verifica se o texto de um elemento identificado pelo ID contém o texto fornecido.

        Args:
            id_element (str): O ID do elemento.
            texto (str): O texto a ser verificado no conteúdo do elemento.

        Returns:
            bool: True se o texto for encontrado, False caso contrário.
        """
        try:
            elemento = self.wait_d.until(presence_of_element_located((By.ID, id_element)))
            return texto in elemento.text
        except Exception:
            return False
