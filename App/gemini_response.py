# ... [Your existing Pinecone/Search code above] ...
# results = dense_index.search(...)

from google import genai
from google.genai import types

# Initialize Gemini Client
# Get your key from: https://aistudio.google.com/
client = genai.Client(api_key="GEMINI_API_KEY")

def generate_answer(query, search_results):
    # 1. Prepare Context (Same as before)
    for hit in search_results['result']['hits']:
        context_text = "\n\n".join(hit['fields']['chunk_text'])
    print("Context prepared")

    # 2. Define System Instructions
    # Gemini uses a specific config parameter for system instructions
    sys_instruction = """
    You are a helpful HR assistant. 
    Answer the user's question using ONLY the context provided below.
    If the answer is not in the context, state that you cannot find it.
    """
    print("Sys instructions set")
    # 3. Create the Prompt
    user_prompt = f"""
    Context Information:
    {context_text}

    User Question: 
    {query}
    """
    print("Prompt created....Attempting to generate response")
    # 4. Call Gemini (Using 1.5-flash for speed/efficiency)
    try:
        print("try conditioned started")
        print("Prompt generation starting...")
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.2, # Low temperature for factual answers
            )
        )
        print("Response created successfully")
        print(response.text)
    except Exception as e:
        return f"Error generating answer: {e}"

if __name__ == "__main__":
    query="test"
    results="Test"
    # --- Run the function ---
    print("\nThinking (Gemini)...")
    final_answer = generate_answer(query, results)

    print("-" * 50)
    print(f"🤖 Gemini Answer:\n{final_answer}")
    print("-" * 50)