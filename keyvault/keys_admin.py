def get_secrets(kvname,secretname):
    import os
    from azure.keyvault.secrets import SecretClient
    from azure.identity import DefaultAzureCredential

    keyVaultName = kvname#os.environ["KEY_VAULT_NAME"]
    KVUri = f"https://{keyVaultName}.vault.azure.net"

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=KVUri, credential=credential)

    retrieved_secret = client.get_secret(secretname)

    return retrieved_secret.value