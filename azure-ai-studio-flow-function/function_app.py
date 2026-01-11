import azure.functions as func
import os
import json
from datetime import datetime
from openai import OpenAI

app = func.FunctionApp()

@app.route(route="ai_studio_flow", auth_level=func.AuthLevel.FUNCTION)
def ai_studio_flow_function(req: func.HttpRequest) -> func.HttpResponse:
    """
    Azure Function that replicates the Azure AI Studio Prompt Flow.
    Processes user questions through GPT and returns structured responses.
    """
    # Get configuration from environment variables
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT")
    deployment_name = os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_key = os.environ.get("AZURE_OPENAI_API_KEY")
    
    # Validate configuration
    if not endpoint:
        return func.HttpResponse(
            json.dumps({"error": "AZURE_OPENAI_ENDPOINT environment variable is not set"}),
            status_code=500,
            mimetype="application/json"
        )
    if not deployment_name:
        return func.HttpResponse(
            json.dumps({"error": "AZURE_OPENAI_DEPLOYMENT_NAME environment variable is not set"}),
            status_code=500,
            mimetype="application/json"
        )
    if not api_key:
        return func.HttpResponse(
            json.dumps({"error": "AZURE_OPENAI_API_KEY environment variable is not set"}),
            status_code=500,
            mimetype="application/json"
        )
    
    try:
        # Get user question from request body
        try:
            req_body = req.get_json()
            user_question = req_body.get("user_question") or req_body.get("message") or req_body.get("question")
            if not user_question:
                user_question = "What is the capital of France?"
        except:
            user_question = "What is the capital of France?"
        
        # Initialize OpenAI client with Azure endpoint
        client = OpenAI(
            base_url=endpoint,
            api_key=api_key
        )
        
        # Create the prompt (matching the chat_with_gpt.jinja2 template)
        system_message = "You are a helpful AI assistant that explains technical concepts clearly."
        user_message = user_question
        
        # Call GPT (matching the flow's chat_with_gpt node)
        completion = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            temperature=1,
            top_p=1
        )
        
        llm_output = completion.choices[0].message.content
        
        # Process response (matching the response.py node logic)
        result = {
            "answer": llm_output,
            "original_query": user_question,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "success" if len(llm_output) > 0 else "failure"
        }
        
        return func.HttpResponse(
            json.dumps(result, indent=2),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        error_result = {
            "error": str(e),
            "status": "failure",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return func.HttpResponse(
            json.dumps(error_result, indent=2),
            status_code=500,
            mimetype="application/json"
        )
