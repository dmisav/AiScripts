# AiScripts

A collection of Azure Functions demonstrating various Azure AI services integration using Python. This repository contains serverless functions that leverage Azure's managed identity authentication for secure access to Azure AI services.

## 📁 Repository Structure

```
AiScripts/
├── azure-text-analytics-function/    # Text Analytics sentiment analysis function
├── [future-functions]/               # Additional Azure Functions will be added here
└── README.md                         # This file
```

---

## 🔍 Azure Text Analytics Function

### Overview
The `azure-text-analytics-function` folder contains an Azure Function that demonstrates how to authenticate and interact with Azure Text Analytics (Language Service) using Managed Identity. The function performs sentiment analysis on text documents.

### Features
- ✅ **Managed Identity Authentication**: Uses `DefaultAzureCredential` for secure, keyless authentication
- ✅ **Sentiment Analysis**: Analyzes text sentiment using Azure Text Analytics API
- ✅ **HTTP Trigger**: Exposes a RESTful endpoint for easy integration
- ✅ **Environment-based Configuration**: Secure configuration using environment variables

### Project Structure
```
azure-text-analytics-function/
├── function_app.py          # Main function code using Azure Functions v2 programming model
├── requirements.txt         # Python dependencies
├── host.json               # Azure Functions host configuration
├── local.settings.json     # Local development settings (git-ignored)
└── .gitignore             # Git ignore rules for sensitive files
```

### Prerequisites
- Python 3.9 or higher
- Azure Functions Core Tools v4
- Azure CLI installed and authenticated (`az login`)
- Azure Text Analytics resource with endpoint URL

### Setup Instructions

1. **Install Azure Functions Core Tools** (if not already installed):
   ```bash
   brew tap azure/functions
   brew install azure-functions-core-tools@4
   ```

2. **Navigate to the function directory**:
   ```bash
   cd azure-text-analytics-function
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   - Copy `local.settings.json.example` to `local.settings.json` (if you create a template)
   - Set your `TEXT_ANALYTICS_ENDPOINT` in `local.settings.json`
   - Example:
     ```json
     {
       "Values": {
         "TEXT_ANALYTICS_ENDPOINT": "https://your-resource.cognitiveservices.azure.com"
       }
     }
     ```

5. **Authenticate with Azure CLI**:
   ```bash
   az login
   ```

6. **Run locally**:
   ```bash
   func start
   ```

7. **Test the function**:
   ```bash
   curl http://localhost:7071/api/text_analytics
   ```

### Security Notes
- ✅ No hardcoded secrets or API keys in source code
- ✅ Uses `DefaultAzureCredential` for authentication
- ✅ `local.settings.json` is git-ignored (contains sensitive configuration)
- ✅ Environment variables used for all configuration
- ⚠️ **Important**: Never commit `local.settings.json` or any files containing secrets

### Deployment to Azure

1. **Create an Azure Function App** (if not already created):
   ```bash
   az functionapp create --resource-group <your-rg> --consumption-plan-location <location> --runtime python --runtime-version 3.9 --functions-version 4 --name <your-function-app-name> --storage-account <your-storage-account>
   ```

2. **Configure Application Settings**:
   ```bash
   az functionapp config appsettings set --name <your-function-app-name> --resource-group <your-rg> --settings TEXT_ANALYTICS_ENDPOINT="https://your-resource.cognitiveservices.azure.com"
   ```

3. **Enable Managed Identity**:
   ```bash
   az functionapp identity assign --name <your-function-app-name> --resource-group <your-rg>
   ```

4. **Grant Text Analytics permissions to Managed Identity**:
   ```bash
   az role assignment create --assignee <managed-identity-principal-id> --role "Cognitive Services User" --scope /subscriptions/<subscription-id>/resourceGroups/<resource-group>/providers/Microsoft.CognitiveServices/accounts/<text-analytics-resource>
   ```

5. **Deploy the function**:
   ```bash
   func azure functionapp publish <your-function-app-name>
   ```

### Dependencies
- `azure-functions`: Azure Functions Python SDK
- `azure-identity`: Azure authentication library
- `azure-ai-textanalytics`: Azure Text Analytics client library

---

## 📝 Template for Future Similar Scripts

When creating new Azure Functions for other AI services, follow this structure:

### New Function Checklist

#### 1. Project Setup
- [ ] Create new folder: `azure-{service-name}-function/`
- [ ] Create `function_app.py` with Azure Functions v2 programming model
- [ ] Create `requirements.txt` with necessary dependencies
- [ ] Create `host.json` (can copy from existing function)
- [ ] Create `local.settings.json` template (git-ignored)
- [ ] Update `.gitignore` if needed

#### 2. Dependencies
- [ ] Add `azure-functions` to requirements.txt
- [ ] Add `azure-identity` for Managed Identity authentication
- [ ] Add service-specific SDK (e.g., `azure-ai-textanalytics`, `azure-ai-vision`, etc.)

#### 3. Authentication Setup
- [ ] Use `DefaultAzureCredential()` for authentication
- [ ] Store endpoint/service URL in environment variables
- [ ] No hardcoded API keys or connection strings
- [ ] Document required Azure permissions/roles

#### 4. Function Implementation
- [ ] Define HTTP route with appropriate auth level
- [ ] Handle environment variable configuration
- [ ] Implement proper error handling
- [ ] Return appropriate HTTP status codes
- [ ] Add basic validation for inputs

#### 5. Configuration
- [ ] Add all configuration to `local.settings.json` (git-ignored)
- [ ] Document required environment variables
- [ ] Provide example/template configuration file

#### 6. Documentation
- [ ] Add section to main README.md describing the function
- [ ] Document prerequisites and setup steps
- [ ] Include deployment instructions
- [ ] Add security considerations
- [ ] Provide usage examples

#### 7. Testing
- [ ] Test locally with `func start`
- [ ] Verify authentication works with Azure CLI login
- [ ] Test error handling scenarios
- [ ] Validate environment variable loading

#### 8. Deployment Preparation
- [ ] Document Azure Function App creation steps
- [ ] List required Application Settings
- [ ] Document Managed Identity setup
- [ ] Document role assignments needed
- [ ] Test deployment process

### Example Service Patterns

#### Text Analytics (✅ Completed)
- Service: Azure Text Analytics / Language Service
- Endpoint pattern: `https://{resource-name}.cognitiveservices.azure.com`
- Required role: `Cognitive Services User`
- SDK: `azure-ai-textanalytics`

#### Future Services to Add:
- [ ] **Azure AI Vision** - Image analysis and OCR
  - SDK: `azure-ai-vision`
  - Endpoint: `https://{resource-name}.cognitiveservices.azure.com`
  
- [ ] **Azure OpenAI Service** - GPT models integration
  - SDK: `azure-openai`
  - Endpoint: `https://{resource-name}.openai.azure.com`
  
- [ ] **Azure Speech Service** - Speech-to-text and text-to-speech
  - SDK: `azure-cognitiveservices-speech`
  - Endpoint: `https://{region}.api.cognitive.microsoft.com`
  
- [ ] **Azure Translator** - Language translation
  - SDK: `azure-ai-translation-text`
  - Endpoint: `https://api.cognitive.microsofttranslator.com`
  
- [ ] **Azure Form Recognizer** - Document analysis
  - SDK: `azure-ai-formrecognizer`
  - Endpoint: `https://{resource-name}.cognitiveservices.azure.com`
  
- [ ] **Azure Face API** - Face detection and recognition
  - SDK: `azure-cognitiveservices-vision-face`
  - Endpoint: `https://{region}.api.cognitive.microsoft.com`

### Common Patterns

#### Environment Variable Pattern
```python
import os
endpoint = os.environ.get("SERVICE_ENDPOINT")
if not endpoint:
    return func.HttpResponse("SERVICE_ENDPOINT not configured", status_code=500)
```

#### Authentication Pattern
```python
from azure.identity import DefaultAzureCredential
credential = DefaultAzureCredential()
client = ServiceClient(endpoint=endpoint, credential=credential)
```

#### Error Handling Pattern
```python
try:
    result = client.operation()
    return func.HttpResponse(f"Success: {result}", status_code=200)
except Exception as e:
    return func.HttpResponse(f"Error: {str(e)}", status_code=500)
```

---

## 🔒 Security Best Practices

1. **Never commit secrets**: Always use `.gitignore` for configuration files containing sensitive data
2. **Use Managed Identity**: Prefer `DefaultAzureCredential` over API keys when possible
3. **Environment variables**: Store all configuration in environment variables, never hardcode
4. **Least privilege**: Grant only necessary permissions to Managed Identity roles
5. **Review dependencies**: Regularly update dependencies and review for security vulnerabilities

---

## 🛠️ Contributing

When adding a new function:

1. Follow the template checklist above
2. Ensure all security best practices are followed
3. Test locally before committing
4. Update this README with your new function documentation
5. Keep function structure consistent with existing examples

---

## 📚 Additional Resources

- [Azure Functions Python Developer Guide](https://docs.microsoft.com/azure/azure-functions/functions-reference-python)
- [Azure Identity Library Documentation](https://docs.microsoft.com/python/api/overview/azure/identity-readme)
- [DefaultAzureCredential Documentation](https://docs.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential)
- [Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local)

---

## 📄 License

[Add your license information here]
