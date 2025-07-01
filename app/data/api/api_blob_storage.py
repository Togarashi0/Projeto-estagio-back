from azure.storage.blob import BlobServiceClient, StandardBlobTier
from azure.core.exceptions import ResourceExistsError
from app.data.api.api_cofre_senhas import ApiCofreSenhas


class AzureBlob:
    def __init__(self, container_name=None):
        credencial = ApiCofreSenhas().obter_login_senha_filtrando_por_login(login="rpa", credencial_id='68003b22993f5c2cc85bcc0e')
        self.connection_string = credencial[1]
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        if container_name:
            self.container_client = self.blob_service_client.get_container_client(container_name)
            try:
                self.container_client.create_container()
            except ResourceExistsError:
                pass
        else:
            self.container_client = None

    def upload_file(self, nome_arquivo: str, data):
        blob_client = self.container_client.get_blob_client(nome_arquivo)
        blob_client.upload_blob(data, overwrite=True)
        blob_client.set_standard_blob_tier(StandardBlobTier.COLD)

    def show_files(self):
        return [{"container": blob.container, "name": blob.name, "size": blob.size, "last_modified": blob.last_modified, "content_type": blob.content_settings.content_type} for blob in
                self.container_client.list_blobs()]

    def list_containers(self):
        return [{"name": container.name, "last_modified": container.last_modified} for container in self.blob_service_client.list_containers()]

    def download_file(self, nome_arquivo: str, download_path: str):
        blob_client = self.container_client.get_blob_client(nome_arquivo)
        with open(download_path, "wb") as file:
            data = blob_client.download_blob()
            file.write(data.readall())

    def download_file_stream(self, nome_arquivo: str):
        blob_client = self.container_client.get_blob_client(nome_arquivo)
        download_stream = blob_client.download_blob()
        return download_stream.readall()
