# prompts.py

PROMPT_VARIANTS = [
    {
        "name": "relevance_v1_zero_shot_minimal",
        "system": (
            "You are a careful research assistant labeling news articles for protest relevance. "
            "Follow the label definitions exactly. Do not add extra text."
        ),
        "user_template": (
            "Task: Label the article as exactly ONE of:\n"
            "- IRRELEVANT\n"
            "- RELEVANT_DIRECT\n"
            "- RELEVANT_INDIRECT\n\n"
            "Definitions:\n"
            "RELEVANT_DIRECT: Primary focus is on coverage of a single specific protest/strike/rally/demonstration "
            "as an event (journalist frames how to understand the protest/protesters).\n"
            "RELEVANT_INDIRECT: Protest is central but covered indirectly via aftermath or response (e.g., politician remarks, "
            "legal proceedings, investigations). Not event coverage itself.\n"
            "IRRELEVANT: Protest/riot/strike is only mentioned briefly or as background/metaphor; or the text is not a real "
            "multi-paragraph article; or the actor is not people engaged in collective action (e.g., sanctions, military groups).\n\n"
            "Output JSON only: {{\"label\": \"IRRELEVANT\"|\"RELEVANT_DIRECT\"|\"RELEVANT_INDIRECT\"}}\n\n"
            "ARTICLE\n"
            "Title: {title}\n"
            "Text:\n"
            "{text}\n"
        ),
    },

    {
        "name": "relevance_v2_zero_shot_two_stage_internal",
        "system": (
            "You label news articles for protest relevance using a two-step decision. "
            "Be consistent and follow the rules. Output JSON only."
        ),
        "user_template": (
            "Step 1 (Relevance): Decide if the article is relevant to a specific protest/strike/rally/demonstration/collective action.\n"
            "Step 2 (If relevant): Decide if it is DIRECT event coverage or INDIRECT aftermath/response coverage.\n\n"
            "Rules:\n"
            "- If protests are only mentioned in passing/background/metaphor: IRRELEVANT.\n"
            "- DIRECT: focuses on the protest event itself; journalists choose what aspects to emphasize.\n"
            "- INDIRECT: focuses on consequences/response (politician remarks, legal case, investigation), where the protest is central.\n\n"
            "Output JSON only: {{\"label\": \"IRRELEVANT\"|\"RELEVANT_DIRECT\"|\"RELEVANT_INDIRECT\"}}\n\n"
            "ARTICLE\n"
            "Title: {title}\n"
            "Text:\n"
            "{text}\n"
        ),
    },

    {
        "name": "relevance_v3_few_shot_trimmed_with_reasons",
        "system": (
            "You label news articles for protest relevance. Use the examples to learn the decision boundary. "
            "Do not copy the examples' wording. Output JSON only."
        ),
        "user_template": (
            "Choose exactly ONE label:\n"
            "- IRRELEVANT\n"
            "- RELEVANT_DIRECT\n"
            "- RELEVANT_INDIRECT\n\n"
            "Definitions:\n"
            "RELEVANT_DIRECT: Main story is a single protest/strike/rally event itself.\n"
            "RELEVANT_INDIRECT: Main story is aftermath/response to a protest (remarks, legal proceedings, investigations).\n"
            "IRRELEVANT: Protest-related term is only brief/background/metaphor; or not a real multi-paragraph article.\n\n"
            "Examples:\n"
            "EXAMPLE A\n"
            "Label: RELEVANT_DIRECT\n"
            "Why: focuses on a single labor action; event coverage; framing choices about stakes/claims.\n"
            "Text (excerpt):\n"
            "\"A strike vote Thursday by the union representing 1,500 stagehands and other backstage workers could shut down Broadway shows...\"\n"
            "\"This strike vote will send a strong message...\" (union president)\n\n"
            "EXAMPLE B\n"
            "Label: RELEVANT_INDIRECT\n"
            "Why: the news is the president's remarks marking the Jan. 6 riot; protest/riot is central but covered via response.\n"
            "Text (excerpt):\n"
            "\"President Biden is speaking at a campaign event... to mark three years since supporters of then-President Donald Trump rioted at the U.S. Capitol...\"\n\n"
            "EXAMPLE C\n"
            "Label: IRRELEVANT\n"
            "Why: 'riots' are only mentioned in passing; the article is about something else.\n"
            "Text (excerpt):\n"
            "\"A British actress has claimed that being called 'woke' is 'as bad' as a racial slur...\"\n"
            "\"I was aware of why [the riots] flared up...\" (brief mention)\n\n"
            "Now label this article.\n"
            "Output JSON only: {{\"label\": \"IRRELEVANT\"|\"RELEVANT_DIRECT\"|\"RELEVANT_INDIRECT\"}}\n\n"
            "ARTICLE\n"
            "Title: {title}\n"
            "Text:\n"
            "{text}\n"
        ),
    },

    {
        "name": "relevance_v4_few_shot_stricter_irrelevant_guardrail",
        "system": (
            "You label protest relevance. Prefer IRRELEVANT when protest is not central. Output JSON only."
        ),
        "user_template": (
            "Labels: IRRELEVANT, RELEVANT_DIRECT, RELEVANT_INDIRECT.\n\n"
            "Guardrail (important): If you cannot point to multiple sentences where the protest/collective action is a main topic, "
            "label IRRELEVANT.\n\n"
            "DIRECT vs INDIRECT:\n"
            "- DIRECT = protest event coverage.\n"
            "- INDIRECT = aftermath/response coverage (remarks, legal action, investigation) where the protest is still central.\n\n"
            "Few-shot anchors:\n"
            "[DIRECT anchor]\n"
            "\"A strike vote... could shut down Broadway shows...\" → RELEVANT_DIRECT\n"
            "[INDIRECT anchor]\n"
            "\"Biden is speaking... to mark... rioted at the U.S. Capitol...\" → RELEVANT_INDIRECT\n"
            "[IRRELEVANT anchor]\n"
            "\"A British actress has claimed...\" with a brief late mention of \"riots\" → IRRELEVANT\n\n"
            "Output JSON only: {{\"label\": \"IRRELEVANT\"|\"RELEVANT_DIRECT\"|\"RELEVANT_INDIRECT\"}}\n\n"
            "ARTICLE\n"
            "Title: {title}\n"
            "Text:\n"
            "{text}\n"
        ),
    },

    {
        "name": "relevance_v5_zero_shot_codebook_style_more_explicit",
        "system": (
            "You are labeling articles for a protest-paradigm dataset. Be literal and conservative. Output JSON only."
        ),
        "user_template": (
            "All articles contain protest-related keywords, but many are irrelevant. Your job is to classify relevance.\n\n"
            "RELEVANT_DIRECT (protest paradigm suitable): primary focus is a single specific protest/strike/rally event itself; "
            "journalist must interpret how to understand the protest/protesters.\n"
            "RELEVANT_INDIRECT (not traditional paradigm but still relevant): focuses on consequences/response to a specific protest "
            "(e.g., politician remarks, legal proceedings, investigation); protest is central but not described as an event.\n"
            "IRRELEVANT: protest is a brief mention/background; expanding protester claims would be off-topic; or text is too short "
            "to be a real article; or actor is not individuals in collective action.\n\n"
            "Return JSON only: {{\"label\": \"IRRELEVANT\"|\"RELEVANT_DIRECT\"|\"RELEVANT_INDIRECT\"}}\n\n"
            "ARTICLE\n"
            "Title: {title}\n"
            "Text:\n"
            "{text}\n"
        ),
    },

    {
        "name": "relevance_v6_two_field_output_with_rationale_tags",
        "system": (
            "Label protest relevance. Output JSON only with a short rationale tag set (not freeform)."
        ),
        "user_template": (
            "Choose one label: IRRELEVANT, RELEVANT_DIRECT, RELEVANT_INDIRECT.\n\n"
            "Definitions:\n"
            "- RELEVANT_DIRECT: protest event coverage.\n"
            "- RELEVANT_INDIRECT: aftermath/response coverage to a specific protest.\n"
            "- IRRELEVANT: only passing mention/background/metaphor, or not a real multi-paragraph article.\n\n"
            "Also choose 1–2 rationale tags from:\n"
            "- EVENT_COVERAGE\n"
            "- AFTERMATH_RESPONSE\n"
            "- PASSING_MENTION\n"
            "- TOO_SHORT_TRUNCATED\n\n"
            "Output JSON only:\n"
            "{{"
            "\"label\":\"IRRELEVANT|RELEVANT_DIRECT|RELEVANT_INDIRECT\","
            "\"tags\":[\"...\"]"
            "}}\n\n"
            "ARTICLE\n"
            "Title: {title}\n"
            "Text:\n"
            "{text}\n"
        ),
    },

]
