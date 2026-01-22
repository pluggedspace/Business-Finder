import os
import json
import re
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def clean_groq_json(text: str):
    """
    Clean Groq response and ensure we extract a list of needs.
    Handles cases where model wraps JSON in markdown or prose.
    """
    # Remove Markdown fences like ```json ... ```
    text = re.sub(r"^```json|```$", "", text.strip(), flags=re.MULTILINE)
    text = text.strip()

    try:
        data = json.loads(text)
        if isinstance(data, dict) and "needs" in data:
            return data["needs"]
        elif isinstance(data, list):
            return data
        else:
            return [str(data)]
    except Exception:
        # Fallback: return as single-item list
        return [text]

def analyze_business(lead):
    """
    Analyze a business using Groq LLM and return possible needs.
    Includes LinkedIn + OSM enrichment.
    """
    # Build a context string with all available data
    linkedin_info = json.dumps(lead.linkedin_data, indent=2) if lead.linkedin_data else "Not available"
    osm_info = json.dumps(lead.osm_data, indent=2) if lead.osm_data else "Not available"

    prompt = f"""
    You are a business consultant AI.
    Analyze the following business and suggest what this business might need
    (in terms of digital solutions, marketing, or operations).

    Business Name: {lead.name}
    Category: {lead.category}
    Address: {lead.address}
    Website: {lead.website or 'Not available'}
    Phone: {lead.phone or 'Not available'}
    Rating: {lead.rating or 'Not available'}

    LinkedIn Data: {linkedin_info}
    OpenStreetMap Data: {osm_info}

    You must ONLY return valid JSON in this exact format:
    {{
        "needs": [
            "Improve website design",
            "Boost social media marketing",
            "Hire more staff"
        ]
    }}

    Do not include explanations, markdown, or any other text.
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=200
    )

    content = response.choices[0].message.content.strip()
    needs = clean_groq_json(content)

    # Save directly to lead
    lead.needs = needs
    lead.save()

    return {"needs": needs}