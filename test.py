import openai, os, requests

openai.api_type = "azure"
# Azure OpenAI on your own data is only supported by the 2023-08-01-preview API version
openai.api_version = "2023-08-01-preview"

# Azure OpenAI setup
openai.api_base = "https://test-open-ai-pdf.openai.azure.com/" # Add your endpoint here
openai.api_key = "97cc24e840fc4de6910ca9e3b90611ce" # Add your OpenAI API key here
deployment_id = "test-deployment" # Add your deployment ID here

# Azure AI Search setup
search_endpoint = "https://aisearchservicejr93.search.windows.net"; # Add your Azure AI Search endpoint here
search_key = "MWSeVOfshKk7vlXkwEZyfuuXpJ4eSYfs4p4i6tC75gAzSeCaMqOD"; # Add your Azure AI Search admin key here
search_index_name = "test-vector-index"; # Add your Azure AI Search index name here

def setup_byod(deployment_id: str) -> None:
    """Sets up the OpenAI Python SDK to use your own data for the chat endpoint.

    :param deployment_id: The deployment ID for the model to use with your own data.

    To remove this configuration, simply set openai.requestssession to None.
    """

    class BringYourOwnDataAdapter(requests.adapters.HTTPAdapter):

        def send(self, request, **kwargs):
            request.url = f"{openai.api_base}/openai/deployments/{deployment_id}/extensions/chat/completions?api-version={openai.api_version}"
            return super().send(request, **kwargs)

    session = requests.Session()

    # Mount a custom adapter which will use the extensions endpoint for any call using the given `deployment_id`
    session.mount(
        prefix=f"{openai.api_base}/openai/deployments/{deployment_id}",
        adapter=BringYourOwnDataAdapter()
    )

    openai.requestssession = session

setup_byod(deployment_id)


message_text = [{"role": "user", "content": "W ktorym roku odbyla sie bitwa pod grunwaldem?"}]

completion = openai.ChatCompletion.create(
    messages=message_text,
    deployment_id=deployment_id,
    dataSources=[  # camelCase is intentional, as this is the format the API expects
        {
            "type": "AzureCognitiveSearch",
            "parameters": {
                "endpoint": search_endpoint,
                "key": search_key,
                "indexName": search_index_name,
            }
        }
    ]
)
print(completion)