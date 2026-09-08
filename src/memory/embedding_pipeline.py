from mistralai.client import Mistral

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])

def embed_text(text: str) -> list[float]:
    embeddings_batch_response = client.embeddings.create(
    model="mistral-embed",
    inputs=["Embed this sentence.", "As well as this one."],
    )
    return embeddings_batch_response.data[0].embedding

