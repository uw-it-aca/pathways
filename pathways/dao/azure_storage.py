# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from azure.storage.blob import ContainerClient
from django.conf import settings


class AzureStorageDAO:
    """
    Data Access Object for Azure Storage.
    This class provides methods to interact with Azure Storage services.
    """

    sas_url = getattr(settings, 'AZURE_BLOB_STORAGE_URL', None)
    client = None

    def __init__(self):
        """
        Initializes the AzureStorageDAO
        """
        self.client = ContainerClient.from_container_url(self.sas_url)

    def list_blobs(self):
        """
        Lists all blobs in the Azure Storage container.
        Returns:
            list: A list of blob names.
        """
        blob_names = []
        for blob in self.client.list_blobs():
            blob_names.append(blob.name)
        return blob_names

    def get_blob(self, blob_name):
        """
        Retrieves a specific blob from the Azure Storage container.
        Args:
            blob_name (str): The name of the blob to retrieve.
        Returns:
            String: The contents of the blob.
        """
        return (self.client.get_blob_client(blob_name)
                .download_blob(encoding='UTF-8').readall())

    def get_most_recent_blob(self):
        """
        Retrieves the most recent blob from the Azure Storage container.
        Returns:
            String: The contents of the most recent blob.
        """
        blobs = self.client.list_blobs()
        most_recent_blob = max(blobs, key=lambda b: b.last_modified)
        return self.get_blob(most_recent_blob.name)
