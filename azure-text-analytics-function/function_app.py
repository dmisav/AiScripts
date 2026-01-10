import azure.functions as func
import os
from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

app = func.FunctionApp()

@app.route(route="text_analytics", auth_level=func.AuthLevel.FUNCTION)
def text_analytics_function(req: func.HttpRequest) -> func.HttpResponse:
    # Get endpoint from environment variable (set in local.settings.json for local dev)
    endpoint = os.environ.get("TEXT_ANALYTICS_ENDPOINT")
    if not endpoint:
        return func.HttpResponse("TEXT_ANALYTICS_ENDPOINT environment variable is not set", status_code=500)

    try:
        # DefaultAzureCredential handles the Managed Identity automatically
        credential = DefaultAzureCredential()
        client = TextAnalyticsClient(endpoint=endpoint, credential=credential)

        # Simple test: Analyze sentiment of a string
        documents = ["I am successfully authenticated using Managed Identity!"]
        result = client.analyze_sentiment(documents=documents)[0]

        return func.HttpResponse(
            f"Auth Success! Sentiment is: {result.sentiment}",
            status_code=200
        )
    except Exception as e:
        return func.HttpResponse(f"Auth Failed: {str(e)}", status_code=500)
