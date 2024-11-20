# Load Type

* Enumerar possíveis fontes de save/load do repositório, para criar opções dentro de outras classes

# Utilizar VertexAI embeddings

* Necessário conta na GCP com billing configurado
* Ativar API VertexAI
* Utilizar Google Cloud SDK:
  * Instalar a CLI do google: https://cloud.google.com/sdk/docs/install?hl=pt-br;
  * Ao executar automaticamente o gcloud init, será setado o usuário, o projeto, e a região default;

    ```
    gcloud auth application-default login
    gcloud config set project seu_project_id
    ```
    Pode ser que precise:
    ```
    gcloud config set billing/quota_project YOUR_PROJECT
    ```
* Usar credenciais ".json" baixadas da GCP
  * Console -> IAM -> Contas de Seviço -> "CRIAR CONTA DE SERVIÇO" (e dar as permissões necessárias) -> entrar na conta de serviço -> "CHAVES" -> "ADICIONAR CHAVE" -> "CRIAR NOVA CHAVE" -> "JSON" -> "CRIAR" -> colocar o .json na pasta "main.credentials"
