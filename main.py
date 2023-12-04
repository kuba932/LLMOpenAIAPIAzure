import os
import openai
import dotenv

dotenv.load_dotenv()

endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
api_key = os.environ.get("AZURE_OPENAI_API_KEY")
deployment = os.environ.get("DEPLOYMENT_MODEL")

client = openai.AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-10-01-preview",
)

completion = client.chat.completions.create(
    model=deployment,
    messages=[
        {
            "role": "user",
            "content": "Kiedy odbyla sie bitwa pod Grunwaldem?",
        },
    ],
    extra_body={
        "dataSources": [
            {
                "type": "AzureCognitiveSearch",
                "parameters": {
                    "endpoint": os.environ["SearchEndpoint"],
                    "key": os.environ["SEARCH_ADMIN_KEY"],
                    "indexName": os.environ["INDEX_NAME"]
                }
            }
        ]
    }
)

print(completion.model_dump_json(indent=2))