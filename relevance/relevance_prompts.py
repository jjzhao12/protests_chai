pmPROMPT = """
You are classifying news articles for relevance to protest-event framing research.

Your task is to determine whether the article is RELEVANT or IRRELEVANT.

Return your answer strictly as valid JSON in ONE of the following two formats:

{
  "label": "RELEVANT"
}

OR

{
  "label": "IRRELEVANT"
}

Do not include any explanation or additional text outside the JSON object.
The JSON must contain exactly one key: "label".

--------------------------------------------------

Definition of RELEVANT:

An article is RELEVANT if:

1. It features at least one protest, demonstration, rally, riot, movement, or civilian collective action,

AND

2. The protest event is referenced, meaning:
   - The protest disrupted an event or prompted a reaction,
   - OR the article discusses political, legal, or public consequences of a specific protest event.

The protest does NOT need to be the primary focus of the article.

Articles about reactions to protests (e.g., politicians responding, celebrities commenting, investigations, legal proceedings) are RELEVANT if they reference a specific protest event.

Protest actors must involve civilian collective action.
Do NOT count:
- Countries imposing sanctions
- Military actions
- Militant or armed groups

--------------------------------------------------

Definition of IRRELEVANT:

An article is IRRELEVANT if:

- It contains only a passing historical reference (e.g., “since the protests of 2020…” with no further detail)
- It mentions “unrest” or protests without describing a specific event
- Protest is background context for another topic
- Protesters are militant or armed groups

--------------------------------------------------

Edge cases of PASSING MENTION (IRRELEVANT):

- “The policy sparked protests last year.” (no further detail)
- “Markets reacted after weeks of unrest.” (no described event)
- “The decision comes amid global protests.” (no specific protest discussed)

If the article references a specific protest event in a meaningful way (even briefly), classify as RELEVANT.

Again, output ONLY valid JSON with exactly one key: "label".

--------------------------------------------------
ARTICLE TO CLASSIFY:

TITLE:
{title}

TEXT:
{text}
"""