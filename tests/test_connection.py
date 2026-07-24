from backend.lm_client import LocalLLMClient

print("Testing Ollama connection...")

client = LocalLLMClient()

if client.test_connection():
    print("✅ Connected successfully!")
else:
    print("❌ Connection failed.")