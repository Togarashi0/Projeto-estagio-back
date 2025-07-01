import re
from datetime import datetime, timedelta


class Utils:
    """Uma classe para várias utilidades de texto e tempo."""

    @staticmethod
    def get_greeting():
        """Retorna uma saudação baseada na hora atual."""
        current_hour = datetime.now().hour
        if 0 <= current_hour <= 11:
            return "Bom dia"
        elif 12 <= current_hour <= 17:
            return "Boa tarde"
        else:
            return "Boa noite"

    @staticmethod
    def capitalize_first_letter(word):
        """Capitaliza a primeira letra de uma palavra."""
        return word[0].upper() + word[1:]

    @staticmethod
    def extract_first_name(email):
        """Extrai o primeiro nome de um endereço de e-mail."""
        parts = email.split('@')
        if len(parts) == 2:
            name_part = parts[0]
            name_parts = name_part.split('.')
            if len(name_parts) > 0:
                first_name = name_parts[0]
                return Utils.capitalize_first_letter(first_name)
        return ""

    @staticmethod
    def calculate_execution_time(start_time: float, end_time: float) -> tuple:
        """
        Calcula o tempo de execução entre dois tempos.

        Args:
            start_time (float): O tempo de início em segundos.
            end_time (float): O tempo de término em segundos.

        Returns:
            tuple: Uma tupla contendo horas, minutos e segundos do tempo de execução.
        """
        total_time_secs = end_time - start_time
        total_time_mins, total_time_secs = divmod(total_time_secs, 60)
        total_time_hours, total_time_mins = divmod(total_time_mins, 60)
        return total_time_hours, total_time_mins, total_time_secs

    @staticmethod
    def calculate_execution_time_str(start_time: float, end_time: float) -> str:
        """
        Calcula o tempo de execução entre dois tempos e retorna uma string formatada.

        Args:
            start_time (float): O tempo de início em segundos.
            end_time (float): O tempo de término em segundos.

        Returns:
            str: O tempo de execução formatado como uma string no formato 'HH:MM:SS'.
        """
        total_time_secs = end_time - start_time
        total_time_mins, total_time_secs = divmod(total_time_secs, 60)
        total_time_hours, total_time_mins = divmod(total_time_mins, 60)
        return f"{total_time_hours:.0f}:{total_time_mins:.0f}:{total_time_secs:.2f}"

    @staticmethod
    def process_text(text):
        """Processa o texto de acordo com uma expressão regular."""
        # Encontrar todas as correspondências na string de entrada
        matches = re.findall(r'\[(.*?)\]|(.+)', text)

        # Iterar sobre as correspondências para verificar qual delas é válida
        for match in matches:
            if match[0]:  # Se houver uma correspondência dentro de colchetes
                return match[0]
            elif match[1]:  # Se não houver colchetes, retornar o texto em si
                return match[1]
        return None  # Retorna None se nenhuma correspondência for encontrada

    @staticmethod
    def calculate_future_date(dias: int = 1, validar_dia_util: bool = True):
        """
        Calcula a data futura adicionando uma quantidade especificada de dias à data atual.
        Se `validar_dia_util` for True, ajusta a data para o próximo dia útil se cair em um sábado ou domingo.

        Args:
            dias (int): Número de dias a serem adicionados à data atual. Default é 1.
            validar_dia_util (bool): Indica se deve validar e ajustar para dias úteis. Default é True.

        Returns:
            datetime: A data futura ajustada.
        """
        data_futura = datetime.now() + timedelta(days=dias)

        if validar_dia_util:
            # Se a data futura cair em um sábado (5) ou domingo (6), ajustar para a próxima segunda-feira
            if data_futura.weekday() == 5:
                data_futura += timedelta(days=2)
            elif data_futura.weekday() == 6:
                data_futura += timedelta(days=1)

        return data_futura
