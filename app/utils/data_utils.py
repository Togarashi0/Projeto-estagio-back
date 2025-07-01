import logging
from datetime import datetime, date
from typing import Union, Optional
from validate_docbr import CPF
import re


class DataUtils:
    """
    Classe utilitária para formatação de datas e validação de CPF.
    """

    @staticmethod
    def format_date_to_dmy(value):
        """
        Formata uma data para o formato "dd/mm/yyyy".

        Args:
            value (datetime): Objeto datetime a ser formatado.

        Returns:
            str: Data formatada no formato "dd/mm/yyyy" se o valor for datetime,
                 None se o valor for None.

        Raises:
            TypeError: Se o tipo do objeto passado como argumento não for datetime ou None.
        """
        if isinstance(value, datetime):
            return value.strftime("%d/%m/%Y")
        elif value is None:
            return None
        else:
            raise TypeError(f"Tipo de objeto não formatável: {type(value)}")

    @staticmethod
    def validate_cpf(received_cpf: str) -> str | None:
        """
        Valida um número de CPF usando a biblioteca validate_docbr.
        Retorna o CPF com pontos e traço se válido, ou None se inválido.

        Args:
            received_cpf (str): Número de CPF a ser validado.

        Returns:
            str | None: CPF formatado se válido, ou None se inválido.
        """
        try:
            # Remove qualquer coisa que não seja dígito
            digits_only = re.sub(r'\D', '', received_cpf)

            cpf = CPF()
            if cpf.validate(digits_only):
                return cpf.mask(digits_only)
            return None
        except Exception as e:
            logging.error(f'Erro no método validate_cpf: {e}')
            return None

    @staticmethod
    def format_nj(nj_field):
        """
        Formata o campo NJ, adicionando ponto entre letras e números, removendo espaços extras,
        removendo 'P' do final, se presente, e convertendo tudo para maiúsculas.
        Exemplo: 'NJ 03', 'NJ03' -> 'NJ.03'
                 'nj.17 P' -> 'NJ.17'
                 'DOP P' -> 'DOP'

        Args:
            nj_field (str): Número do núcleo a ser formatado.

        Returns:
            str: Número do núcleo formatado ou "nao_cadastrado" se o valor for inválido.
        """
        if nj_field is None:
            return "nao_cadastrado"

        # Remover espaços extras no início e no final e converter para maiúsculas
        nj_field = nj_field.strip().upper()
        if not nj_field:
            return "nao_cadastrado"  # Retorna "nao_cadastrado" se o valor estiver vazio após remover espaços

        # Remover o "P" do final, se presente, junto com qualquer espaço antes dele
        nj_field = re.sub(r'\s*P$', '', nj_field)

        # Usar expressão regular para capturar letras seguidas de números e adicionar um ponto
        match = re.match(r"^([A-Z]+)[\s]*([0-9]+)$", nj_field)
        if match:
            return f"{match.group(1)}.{match.group(2)}"

        # Caso não corresponda ao padrão esperado
        return nj_field

    @staticmethod
    def format_full_date(input_date: Union[datetime, str]) -> Optional[str]:
        """
        Formata uma data em formato "dd/mm/yyyy hh:mm:ss".

        Args:
            input_date (Union[datetime, str]): data a ser formatada, pode ser um datetime ou uma string.

        Returns:
            Optional[str]: data formatada como string ou None se a formatação falhar.
        """
        try:
            if isinstance(input_date, datetime):
                return input_date.strftime("%d/%m/%Y %H:%M:%S")
            elif isinstance(input_date, str):
                try:
                    parsed_date = datetime.strptime(input_date, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    parsed_date = datetime.strptime(input_date, "%Y-%m-%d")
                return parsed_date.strftime("%d/%m/%Y %H:%M:%S")
            elif isinstance(input_date, date):
                return datetime.combine(input_date, datetime.min.time()).strftime("%d/%m/%Y %H:%M:%S")
            return None
        except (ValueError, TypeError) as e:
            logging.error(f"Erro ao formatar data: {e}")
            return None

    @staticmethod
    def parse_date_dmy_to_datetime(value):
        """
        Converte uma string no formato "dd/mm/yyyy" para um objeto datetime.

        Args:
            value (str): Data no formato "dd/mm/yyyy".

        Returns:
            datetime: Objeto datetime correspondente à data fornecida.

        Raises:
            ValueError: Se o formato da data não for "dd/mm/yyyy".
        """
        try:
            return datetime.strptime(value, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Formato de data inválido: {value}. Esperado 'dd/mm/yyyy'.")

    @staticmethod
    def ensure_datetime(value: date | datetime | None) -> datetime | None:
        """
        Garante que o valor fornecido seja um objeto datetime.

        Args:
            value (date | datetime | None): Valor a ser convertido. Pode ser um objeto date, datetime ou None.

        Returns:
            datetime | None: Retorna o objeto datetime correspondente ao valor fornecido,
                             ou None se o valor for None.
        """
        if value is None:
            return None
        return value if isinstance(value, datetime) else datetime.combine(value, time.min)
