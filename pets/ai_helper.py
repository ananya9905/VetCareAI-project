import requests

def get_ai_assessment(symptoms, answers):
    prompt = f"""
    You are a veterinary triage assistant.
    You must not provide a definitive diagnosis or medication dosage.
    Give safe, simple guidance and recommend consulting a qualified veterinarian.
    
    Pet symptoms:
    {symptoms}
    
    Additional answers:
    {answers}
    
    Provide your response using this structure:
    
    1. Possible concerns
    2. Risk explanation
    3. What the pet owner should do now
    4. When to contact a veterinarian urgently
    5. Important precautions
    
    Keep the answer clear and suitable for a pet owner.
    """
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json = {
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False,
        },
        timeout = 120,
    )
    
    response.raise_for_status()
    
    data = response.json()
    return data["response"]