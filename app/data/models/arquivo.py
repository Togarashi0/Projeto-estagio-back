from datetime import datetime
from mongoengine import StringField

from app.data.api.api_blob_storage import AzureBlob
from app.data.api.sharepoint import Sharepoint
from app.data.models import BaseModel


class Arquivo(BaseModel):
    meta = {'collection': 'arquivos'}

    nome_arquivo: str = StringField(required=True)
    extensao: str = StringField(required=True)
    categoria = StringField(required=True, choices=('SCREENSHOT', 'ANEXO', 'PLANILHA-INGESTAO', 'PLANILHA', 'OUTROS'))

    s3_access_key_id: str = StringField()
    s3_secret_access_key_id: str = StringField()
    s3_region: str = StringField()
    s3_local_file_path: str = StringField()
    s3_bucket_name: str = StringField()

    blob_bucket_name: str = StringField()
    blob_local_file_path: str = StringField()
    blob_connection_string: str = StringField()

    sharepoint_path: str = StringField()
    sharepoint_name: str = StringField()
    sharepoint_site: str = StringField()

    def salvar_arquivo_blobstorage(self, arquivo_bytes: bytes, nome_arquivo: str, extencao: str = ".png", categoria: str = "SCREENSHOT", blob_bucket_name: str = "screenshots"):
        # Salva parcialmente para gerar o ID
        self.nome_arquivo = nome_arquivo
        self.extensao = extencao
        self.categoria = categoria
        self.save()  # Agora self.id existe
        filename = f"{nome_arquivo}-{str(self.id)}{extencao}"
        try:
            ab = AzureBlob(container_name=blob_bucket_name)
            ab.upload_file(filename, arquivo_bytes)
        except Exception as e:
            raise RuntimeError(f"Erro ao enviar arquivo para o blob: {str(e)}")
        else:
            try:
                # Salva definitivomente
                self.nome_arquivo = filename
                self.extensao = extencao
                self.categoria = categoria
                self.blob_bucket_name = blob_bucket_name
                self.blob_connection_string = ab.connection_string
                self.save()
                return self  # <- Retorna a instância do arquivo
            except Exception as e:
                raise RuntimeError(f"Erro ao enviar arquivo para o blob: {str(e)}")

    def salvar_arquivo_sharepoint(self, arquivo_b64: str, site: str, diretorio: str, nome_arquivo: str, extencao: str = ".png",  categoria: str = "SCREENSHOT"):
        # Melhorar esse método deixar de modo generico
        sharepoint = Sharepoint()
        if site == 'NucleoJuridico-CSC' and diretorio == "/Robo de Calculo/2- Arquivos/":
            pasta_nome: str = datetime.now().strftime("%Y-%m-%d")
            full_path = f"{diretorio}{pasta_nome}"
            pastas = sharepoint.search_folder_in_folder(site, diretorio)
            if pasta_nome not in pastas:
                sharepoint.create_folder(site, diretorio, pasta_nome)
        else:
            full_path = diretorio

        sharepoint.upload_base64(site, full_path, arquivo_b64, nome_arquivo)

        self.nome_arquivo = nome_arquivo
        self.extensao = extencao
        self.categoria = categoria
        self.sharepoint_path = full_path
        self.sharepoint_name = nome_arquivo
        self.sharepoint_site = site
        self.save()
        return self

    def to_dict(self):
        """
            Converte o objeto Arquivos para um dicionário com tratamento de None.
            Retorna:
                dict: Dicionário com todos os campos do arquivo, garantindo valores padrão para campos None.
        """
        # Campos básicos sempre presentes
        result = {
            'id': str(self.id),
            'nome_arquivo': self.nome_arquivo,
            'extensao': self.extensao,
            'categoria': self.categoria
        }

        # Campos opcionais de S3
        if hasattr(self, 's3_access_key_id') and self.s3_access_key_id:
            result.update({
                's3_access_key_id': self.s3_access_key_id,
                's3_secret_access_key_id': self.s3_secret_access_key_id,
                's3_region': self.s3_region,
                's3_local_file_path': self.s3_local_file_path,
                's3_bucket_name': self.s3_bucket_name
            })

        # Campos opcionais de Blob Storage
        if hasattr(self, 'blob_bucket_name') and self.blob_bucket_name:
            result.update({
                'blob_bucket_name': self.blob_bucket_name,
                'blob_local_file_path': self.blob_local_file_path,
                'blob_connection_string': self.blob_connection_string
            })

        # Campos opcionais de SharePoint
        if hasattr(self, 'sharepoint_path') and self.sharepoint_path:
            result.update({
                'sharepoint_path': self.sharepoint_path,
                'sharepoint_name': self.sharepoint_name,
                'sharepoint_site': self.sharepoint_site
            })

        return result