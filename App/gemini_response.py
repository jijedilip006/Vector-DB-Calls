# ... [Your existing Pinecone/Search code above] ...
# results = dense_index.search(...)

from google import genai
from google.genai import types
import os


# Initialize Gemini Client
# Get your key from: https://aistudio.google.com/
api_key=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_answer(query, search_results):
    # --- FIX 1: Correctly joining the context ---
    # Extract just the text from the hits into a list
    chunks = [hit['fields']['chunk_text'] for hit in search_results['result']['hits']]
    
    # Join the list into one big string
    context_text = "\n\n".join(chunks)

    # 2. Define System Instructions
    sys_instruction = """
    You are a helpful HR assistant. 
    Answer the user's question using ONLY the context provided below.
    If the answer is not in the context, state that you cannot find it.
    """

    # 3. Create the Prompt
    user_prompt = f"""
    Context Information:
    {context_text}

    User Question: 
    {query}
    """

    # 4. Call Gemini
    try:
        # Ensure your API Key is actually set here!
        # If you are using "GEMINI_API_KEY" literally, it will fail.
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.2,
            )
        )
        print(response.text)  # Return the text to the main script
        
    except Exception as e:
        # This will catch invalid API keys or connection errors
        print(f"Error generating answer: {e}")

if __name__ == "__main__":
    query="test"
    results="Test"
    # --- Run the function ---
    print("\nThinking (Gemini)...")
    final_answer = generate_answer(query, results)

    print("-" * 50)
    print(f"🤖 Gemini Answer:\n{final_answer}")
    print("-" * 50)

if __name__ == "__main__":
    query="test"
    results="Test"
    # --- Run the function ---
    print("\nThinking (Gemini)...")
    final_answer = generate_answer(query, results)

    print("-" * 50)
    print(f"🤖 Gemini Answer:\n{final_answer}")
    print("-" * 50)