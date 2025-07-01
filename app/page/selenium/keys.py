import time
from abc import ABC

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


class KeysAbstract(ABC):
    def __init__(self, webbot, wait_d, wait_r):
        self.webbot = webbot
        self.wait_d = wait_d
        self.wait_r = wait_r

    def esc(self):
        """
        Envia a tecla 'ESC' para a página atual.
        """
        action = ActionChains(self.webbot)
        action.send_keys(Keys.ESCAPE)
        action.perform()

    def enter(self):
        """
        Envia a tecla 'ENTER' para a página atual.
        """
        action = ActionChains(self.webbot)
        action.send_keys(Keys.ENTER)
        action.perform()

    def pag_down(self):
        """
        Envia a tecla 'PAGE DOWN' para a página atual.
        """
        action = ActionChains(self.webbot)
        action.send_keys(Keys.PAGE_DOWN)
        action.perform()

    def scroll_para_direita(self, qtd: int):
        """
        Rola a página para a direita.

        Args:
            qtd (int): A quantidade de vezes para pressionar a tecla de seta para a direita.
        """
        actions = ActionChains(self.webbot)
        for _ in range(qtd):
            actions.send_keys(Keys.ARROW_RIGHT)
        actions.perform()

    def scroll_para_esquerda(self, qtd: int):
        """
        Rola a página para a esquerda.

        Args:
            qtd (int): A quantidade de vezes para pressionar a tecla de seta para a esquerda.
        """
        actions = ActionChains(self.webbot)
        for _ in range(qtd):
            actions.send_keys(Keys.ARROW_LEFT)
        actions.perform()

    def scroll_para_cima(self, qtd: int):
        """
        Rola a página para cima.

        Args:
            qtd (int): A quantidade de vezes para pressionar a tecla de seta para cima.
        """
        actions = ActionChains(self.webbot)
        for _ in range(qtd):
            actions.send_keys(Keys.ARROW_UP)
        actions.perform()

    def scroll_para_baixo(self, qtd: int):
        """
        Rola a página para baixo.

        Args:
            qtd (int): A quantidade de vezes para pressionar a tecla de seta para baixo.
        """
        actions = ActionChains(self.webbot)
        for _ in range(qtd):
            actions.send_keys(Keys.ARROW_DOWN)
        actions.perform()

    def tecla_combinada(self, *teclas):
        """
        Envia uma combinação de teclas para a página atual.

        Args:
            *teclas (str): As teclas a serem enviadas, como 'CTRL', 'SHIFT', 'A', etc.
        """
        action = ActionChains(self.webbot)
        for tecla in teclas:
            action.key_down(tecla)
        action.perform()
        for tecla in teclas:
            action.key_up(tecla)
        action.perform()

    def tecla_tempo(self, tecla, tempo):
        """
        Envia uma tecla para a página atual e aguarda um determinado tempo.

        Args:
            tecla (str): A tecla a ser enviada.
            tempo (float): O tempo em segundos para aguardar após enviar a tecla.
        """
        action = ActionChains(self.webbot)
        action.send_keys(tecla)
        action.perform()
        time.sleep(tempo)
