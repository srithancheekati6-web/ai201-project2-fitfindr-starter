# FitFindr — planning.md

> Complete this document before writing any implementation code.
> Your spec and agent diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Your planning.md will be reviewed as part of your submission.
> Update it before starting any stretch features.

---

## Tools

List every tool your agent will use. For each tool, fill in all four fields.
You must have at least 3 tools. The three required tools are listed — add any additional tools below them.

### Tool 1: search_listings

**What it does:**
Searches the listings dataset and finds secondhand clothing items that match the user's description, size preference, and maximum budget. Results are ranked by keyword relevance so the best match appears first.

**Input parameters:**

- `description` (str): Keywords describing the item the user wants
- `size` (str): Clothing size filter. If None, all sizes are considered.
- `max_price` (float): Maximum price the user is willing to pay. If None, all prices are considered.

**What it returns:**
A list of matching listing dictionaries sorted by relevance score. Each listing contains:

id
title
description
category
style_tags
size
condition
price
colors
brand
platform

**What happens if it fails or returns nothing:**
Returns an empty list. The planning loop stops and displays a helpful error message asking the user to adjust filters or increase the budget.

---

### Tool 2: suggest_outfit

**What it does:**
Uses the selected listing and the user's wardrobe to generate outfit recommendations. The tool uses an LLM to create styling suggestions based on the clothing pieces available.

**Input parameters:**
<!-- List each parameter, its type, and what it represents -->
- `new_item` (dict): The selected listing returned from search_listings().
- `wardrobe` (dict): The user's wardrobe containing clothing items and style information.

**What it returns:**
A text response containing one or more complete outfit suggestions.

**What happens if it fails or returns nothing:**
If the wardrobe is empty, the tool generates general styling advice instead of wardrobe-specific recommendations.

---

### Tool 3: create_fit_card

**What it does:**
Creates a short social-media style caption describing the outfit and the thrifted item. The caption is designed to be shareable and sound like a real outfit post.

**Input parameters:**
- `outfit` (str): Outfit suggestion text returned by suggest_outfit().

**What it returns:**
A 2–4 sentence caption suitable for Instagram, TikTok, or other social media platforms.

**What happens if it fails or returns nothing:**
Returns a descriptive error message if the outfit information is missing or incomplete.

---


## Planning Loop

**How does your agent decide which tool to call next?**
1. Create a new session dictionary.
2. Parse the user query to extract a description, size, and maximum price.
3. Call search_listings() using the parsed values.
4. If no results are found, store an error message and stop the workflow.
5. Select the highest-ranked listing and store it as selected_item.
6. Call suggest_outfit() using the selected item and wardrobe.
7. Store the returned outfit suggestion.
8. Call create_fit_card() using the outfit suggestion and selected item.
9. Store the generated fit card.
10. Return the completed session.

The workflow ends when a fit card is successfully generated or when an error causes early termination.

---

## State Management

**How does information from one tool get passed to the next?**
The agent uses a session dictionary as the single source of truth throughout the interaction.

The session stores:

Original user query
Parsed description, size, and price filters
Search results
Selected listing
User wardrobe
Outfit suggestion
Fit card
Error messages

After each tool finishes, its output is saved in the session and becomes input for the next tool. This ensures all information remains available throughout the interaction.
---

## Error Handling

For each tool, describe the specific failure mode you're handling and what the agent does in response.

| Tool | Failure mode | Agent response |
|------|-------------|----------------|
| search_listings | No results match the query |Store an error message and stop the workflow |
| suggest_outfit | Wardrobe is empty |Generate general styling advice instead of wardrobe-based suggestions |
| create_fit_card | Outfit input is missing or incomplete |Return a descriptive error message explaining why the fit card could not be generated|

---

## Architecture

flowchart TD A[User Query] A --> B[Planning Loop] B --> C[Parse Query] C --> D[search_listings] D --> E{Results Found?} E -->|No| F[Store Error] F --> G[Return Session] E -->|Yes| H[Store selected_item] H --> I[suggest_outfit] I --> J[Store outfit_suggestion] J --> K[create_fit_card] K --> L[Store fit_card] L --> M[Return Session] H -.-> N[Session State] I -.-> N K -.-> N

---

## AI Tool Plan

**Milestone 3 — Individual tool implementations:**
 I will use ChatGPT to help implement each tool separately. For search_listings(), I will provide the tool specification, expected inputs, outputs, and failure behavior. I will verify the implementation by testing multiple search queries and confirming that filtering and ranking work correctly.

For suggest_outfit(), I will provide the wardrobe schema, listing structure, and desired output format. I will verify that the generated outfit suggestions use wardrobe items when available and provide general styling advice when the wardrobe is empty.

For create_fit_card(), I will provide the style requirements and expected caption format. I will verify that the generated caption includes the selected item, platform, price, and outfit vibe.

**Milestone 4 — Planning loop and state management:**
I will use ChatGPT to generate the planning loop implementation based on the Planning Loop, State Management, and Architecture sections. I will verify that the session dictionary is updated correctly, that information flows between tools properly, and that error paths stop execution when appropriate.

---

## A Complete Interaction (Step by Step)

Write out what a full user interaction looks like from start to finish — tool call by tool call. Use a specific example query.

**Example user query:** "I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?"

**Step 1:**
The agent creates a new session and parses the query. It extracts the description "vintage graphic tee" and the maximum price of $30.

**Step 2:**
The agent calls:

search_listings("vintage graphic tee", None, 30)

The tool searches the dataset and returns matching listings sorted by relevance.

**Step 3:**
The agent selects the highest-ranked listing and stores it as selected_item in the session.

**Step 4:**
The agent calls:

suggest_outfit(selected_item, wardrobe)

The tool generates outfit suggestions using pieces from the user's wardrobe.

**Step 5:**
The returned outfit suggestion is stored in the session.

**Step 6:**
The agent calls:

create_fit_card(outfit_suggestion, selected_item)

The tool generates a social-media style caption.

**Step 7:**
The fit card is stored in the session and the completed session is returned.

Final output to user:

**Final output to user:**
The user sees:

The top matching thrifted item.
Outfit recommendations using their wardrobe.
A shareable fit card caption describing the outfit and overall style.
