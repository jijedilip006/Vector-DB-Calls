from google import genai
from google.genai import types
import os


# Initialize Gemini Client
api_key=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_answer(query, search_results):
    chunks = [hit['fields']['chunk_text'] for hit in search_results['result']['hits']]

    context_text = "\n\n".join(chunks)

    # Define System Instructions
    sys_instruction = """
    You are a helpful HR assistant. 
    Answer the user's question using ONLY the context provided below and if it is a generic conversation started then answer with a cheerful tone.
    Format your response using the following:
    - Use bullet points or numbered lists for steps.
    - Ensure each step is on a new line.
    - Format the text based on user prompt only if prompted, if not give as plain text
    If the answer is not in the context, state that you cannot find it.
    """

    
    user_prompt = f"""
    Context Information:
    {context_text}

    User Question: 
    {query}
    """

    # Call Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=sys_instruction,
                temperature=0.2,
            )
        )
        print(response.text)  # Return the text to the main script
        return response.text
        
    except Exception as e:
        # This will catch invalid API keys or connection errors
        print(f"Error generating answer: {e}")

if __name__ == "__main__":
    query="test"
    results="Test"
    print("\nThinking (Gemini)...")
    final_answer = generate_answer(query, results)

    print("-" * 50)
    print(f"🤖 Gemini Answer:\n{final_answer}")
    print("-" * 50)

if __name__ == "__main__":
    query="test"
    results="Test"
    print("\nThinking (Gemini)...")
    final_answer = generate_answer(query, results)

    print("-" * 50)
    print(f"🤖 Gemini Answer:\n{final_answer}")
    print("-" * 50)