import azure.functions as func
import os
from openai import OpenAI

app = func.FunctionApp()

@app.route(route="openai_chat", auth_level=func.AuthLevel.FUNCTION)
def openai_chat_function(req: func.HttpRequest) -> func.HttpResponse:
    # Get configuration from environment variables
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    
    # Validate configuration
    if not endpoint:
        return func.HttpResponse("AZURE_OPENAI_ENDPOINT environment variable is not set", status_code=500)
    if not deployment_name:
        return func.HttpResponse("AZURE_OPENAI_DEPLOYMENT_NAME environment variable is not set", status_code=500)
    if not api_key:
        return func.HttpResponse("AZURE_OPENAI_API_KEY environment variable is not set", status_code=500)
    
    try:
        # Initialize OpenAI client with Azure endpoint
        client = OpenAI(
            base_url=endpoint,
            api_key=api_key
        )
        
        # Get user message from request body or use default
        try:
            req_body = req.get_json()
            user_message = req_body.get("message", "What is the capital of France?")
        except:
            user_message = "What is the capital of France?"
        
        # Create chat completion
        completion = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
        )
        
        response_message = completion.choices[0].message.content
        
        return func.HttpResponse(
            response_message,
            status_code=200,
            mimetype="text/plain"
        )
    except Exception as e:
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)
