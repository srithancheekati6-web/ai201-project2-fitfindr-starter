"""
tools.py

The three required FitFindr tools. Each tool is a standalone function that
can be called and tested independently before being wired into the agent loop.

Complete and test each tool before moving to agent.py.

Tools:
    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)              → str
    create_fit_card(outfit, new_item)               → str
"""

import os

from dotenv import load_dotenv
from groq import Groq

from utils.data_loader import load_listings

load_dotenv()


# ── Groq client ───────────────────────────────────────────────────────────────

def _get_groq_client():
    """Initialize and return a Groq client using GROQ_API_KEY from .env."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError(
            "GROQ_API_KEY not set. Add it to a .env file in the project root."
        )
    return Groq(api_key=api_key)


# ── Tool 1: search_listings ───────────────────────────────────────────────────

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:

    listings = load_listings()

    keywords = description.lower().split()

    scored = []

    for item in listings:

        if max_price is not None:
            if item["price"] > max_price:
                continue

        if size:
            if size.lower() not in item["size"].lower():
                continue

        text = (
            item["title"] + " " +
            item["description"] + " " +
            " ".join(item["style_tags"])
        ).lower()

        score = sum(
            1 for word in keywords
            if word in text
        )

        if score > 0:
            scored.append((score, item))

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return [item for score, item in scored]

# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:

    client = _get_groq_client()

    items = wardrobe.get("items", [])

    if not items:

        prompt = f"""
        Give styling advice for this thrifted item:

        {new_item['title']}

        Give 2 outfit ideas.
        """

    else:

        wardrobe_text = "\n".join(
            item["name"] for item in items
        )

        prompt = f"""
        New item:

        {new_item['title']}

        User wardrobe:

        {wardrobe_text}

        Suggest 2 complete outfits using the new item.
        """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:

    if not outfit or not outfit.strip():
        return "Unable to generate fit card because outfit data is missing."

    client = _get_groq_client()

    prompt = f"""
    Create a casual Instagram caption.

    Item:
    {new_item['title']}

    Price:
    ${new_item['price']}

    Platform:
    {new_item['platform']}

    Outfit:
    {outfit}

    Make it sound natural and stylish.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=1.0
    )

    return response.choices[0].message.content