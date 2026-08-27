THEORETICAL_FRAMES_PROMPT = """
You are coding news coverage of protest events for a research project on media framing.

You will receive two inputs:

TITLE: the title of a news article.
EXCERPT: a truncated excerpt from the news article.

The EXCERPT is not the full article. It consists of text surrounding mentions of protests,
demonstrations, strikes, rallies, or related protest activity. Make all classifications using
ONLY the provided TITLE and EXCERPT. Do not use outside knowledge or infer information
that is not supported by the provided text.

All samples contain at least one protest or potentially multiple protests. First identify the
relevant protest event or events, who the protesters are, and which people or organizations
qualify as authority figures.

You must code two variables:

1. title_frame
2. excerpt_frame


==================================================
TITLE AND EXCERPT FRAMING
==================================================

Assign exactly ONE frame to the TITLE and exactly ONE frame to the EXCERPT.

The guiding theoretical question is:

    How does the journalist want the reader to understand this protest event
    or the protesters involved?

Journalists will rarely explicitly state their own opinion. Framing instead emerges from what
information, details, descriptions, quotations, and perspectives they choose to include,
exclude, and emphasize.

The possible frames are:

PROTESTER VIOLENCE
The protest or protesters are presented through protesters committing physical or verbal
violence against people.

HARM TO PROTESTERS
The protest or protesters are presented through protesters being harmed, injured,
victimized, or unjustly treated.

PROPERTY DAMAGE
The protest is presented through destruction, vandalism, looting, arson, or other
material/property damage.

DISRUPTION
The protest is presented through interruption of normal social, economic, or civic
activity, including disruptive spectacle.

GRIEVANCE
The protest is presented through protesters' substantive demands, complaints, policy
goals, or desire for change.

WIDESPREAD SUPPORT
The protest is presented through popularity, turnout, scale, or broader public backing.

PEACEFUL
The protest is presented as orderly, calm, peaceful, or nonviolent.

IMPACTFUL
The protest and protesters are presented in terms of longer-term institutional, policy,
or economic consequences. Protesters are depicted as agents producing impact.

RESIDUAL
None of the predefined frames meaningfully characterize how the journalist presents
the protest or protesters.


GENERAL FRAMING PRINCIPLES

A protest's inherent characteristics are not by themselves sufficient to establish a frame.
For example:

- Arrests alone do NOT establish Harm to Protesters.
- A strike alone does NOT establish Disruption.
- A walkout or hunger strike alone does NOT establish Peaceful.
- Calling an event a "riot" or "insurrection" alone does NOT establish Protester Violence.

The classification concerns how the journalist PRESENTS the protest, not merely the
objective characteristics of the protest event.


TITLE FRAME

Ask:

    How does this title contribute to how I interpret the protest event or protesters?

Take the title at face value.

If the title does not mention or meaningfully represent the protest or protesters,
title_frame MUST be "residual".

This is NOT simply a keyword test. For example, a title describing "anti-fascists"
blocking a government hearing clearly describes protesters even if it does not use
the words "protest" or "protester".

If the title presents a protest/protesters through one of the frames, select that frame.
If multiple frames are present, select the most prominent one.

Every title MUST receive exactly one of the nine permitted frame labels, including
"residual" when none of the other frames applies.


EXCERPT FRAME

Ask:

    How does the journalist want me to understand or remember this protest event
    and its protesters?

The excerpts are short windows surrounding protest mentions rather than complete articles.
Therefore, meaningful framing cues within the provided excerpt can be sufficient.

Consider the journalist's selection and emphasis of details, descriptions, quotations,
and other information.

If multiple frames are present, select the DOMINANT frame.

If none of the eight substantive frames meaningfully applies, excerpt_frame MUST be
"residual".

Every excerpt MUST receive exactly one of the nine permitted frame labels.


==================================================
STRICT OUTPUT FORMAT
==================================================

Return ONLY a valid JSON object.

Do NOT include:
- explanations
- reasoning
- markdown
- code fences
- commentary
- any text before or after the JSON object

The JSON object MUST contain exactly these two keys:

{
  "title_frame": "<frame>",
  "excerpt_frame": "<frame>"
}

For title_frame and excerpt_frame, <frame> MUST be exactly ONE of:

"protester_violence"
"harm_to_protesters"
"property_damage"
"disruption"
"grievance"
"widespread_support"
"peaceful"
"impactful"
"residual"

You MUST select exactly one of these frame labels for title_frame and exactly one for
excerpt_frame. Do not return null, N/A, multiple frames, or any other value.
"""

THEORETICAL_BINARY_PROMPT = """
You are coding news coverage of protest events for a research project on media framing.

You will receive two inputs:

TITLE: the title of a news article.
EXCERPT: a truncated excerpt from the news article.

The EXCERPT is not the full article. It consists of text surrounding mentions of protests,
demonstrations, strikes, rallies, or related protest activity. Make all classifications using
ONLY the provided TITLE and EXCERPT. Do not use outside knowledge or infer information
that is not supported by the provided text.

All samples contain at least one protest or potentially multiple protests. First identify the
relevant protest event or events, who the protesters are, and which people or organizations
qualify as authority figures.

You must code three variables:

1. demands_present
2. protester_quote
3. authority_quote


==================================================
DEMANDS PRESENT
==================================================

Determine whether protester demands or goals are substantively communicated.

Code "yes" when the excerpt makes an intentional effort to communicate what protesters
want, what they oppose, why they are protesting, or the goals motivating the protest.

This must go beyond merely recounting events or attaching a broad descriptive label
to the protest.

For example, simply saying that an election occurred and protesters rallied afterward
does not necessarily explain their demands. Likewise, a label such as "anti-Israel
protests" is insufficient by itself.

A substantive protester quote explaining what protesters want can establish demands_present.

The objective does NOT have to constitute a normatively legitimate grievance. A description
of what protesters or rioters sought to accomplish can qualify even if that objective would
not qualify for the Grievance frame.

Return ONLY "yes" or "no" for this variable.


==================================================
QUOTED VOICES
==================================================

Quotes may be spoken or written.

A quote can be:

1. Direct quotation.
2. Indirect reported speech clearly attributed to a specific person or organization.
3. A specific written statement, social media post, or other attributable written speech.

The speech does not have to be verbatim. However, it MUST refer to a specific attributable
speech or writing event rather than merely the journalist's interpretation of someone's
general position.


PROTESTER QUOTE

For protester_quote, the source of the quote MUST actually be a protester, protest organizer,
or protesting group/organization associated with the protest.

Qualifying sources include:

- Individuals participating in the protest.
- Protest organizers.
- Statements issued by the protesting group or organization.

Do NOT count as protester quotes:

- Experts or pundits merely analyzing the protest.
- Politicians merely reacting to the protest.
- Bystanders or observers who are not protesters.
- General crowd chants.
- Protest signs.

The key rule is:

    A protester quote MUST come from a protester, protest organizer,
    or protesting group/organization.

A person who is normally an authority figure can ALSO qualify as a protester if the provided
text depicts that person as participating in or organizing the protest. In that case, their
attributable speech may count for BOTH protester_quote and authority_quote.

Return ONLY "yes" or "no" for this variable.


AUTHORITY QUOTE

For authority_quote, the quoted person or organization must qualify as an authority figure,
public figure, institution, or other actor with social, political, governmental, corporate,
or similar authority.

IMPORTANT:

    The authority figure does NOT need to be involved in the protest.
    The authority figure does NOT need to be the target of the protest.
    The authority figure does NOT need to exercise authority over the protesters.

They may be ANY qualifying authority or public figure whose attributable speech appears
in the excerpt.

Examples can include:

- Government officials and politicians.
- Governmental bodies.
- Law enforcement.
- Supreme Court justices or other high-level public officials.
- Universities or university officials.
- Companies or official company statements.
- Corporate executives.
- Celebrities or other prominent public figures.
- Experts or pundits speaking with public authority or prominence.
- Official institutional statements.
- Attributable government positions or statements.

A celebrity, politician, government official, or other authority figure commenting on a
protest can therefore count as an authority quote even if that person has no direct role
in the protest.

Do NOT count:

- An authority or organization merely declining to comment.
- A report that journalists sought comment but received none.
- A protest organizer who is not otherwise an authority/public figure.
- A statement from a protest group merely because it is an organization.
- An attorney in a court case merely by virtue of being an attorney.

A person can qualify for BOTH protester_quote and authority_quote if they independently
satisfy both definitions.

Return ONLY "yes" or "no" for this variable.


==================================================
STRICT OUTPUT FORMAT
==================================================

Return ONLY a valid JSON object.

Do NOT include:
- explanations
- reasoning
- markdown
- code fences
- commentary
- any text before or after the JSON object

The JSON object MUST contain exactly these three keys:

{
  "demands_present": "<yes_or_no>",
  "protester_quote": "<yes_or_no>",
  "authority_quote": "<yes_or_no>"
}

For demands_present, protester_quote, and authority_quote,
the value MUST be exactly:

"yes"

or

"no"

Do not return true/false, 1/0, null, N/A, or any other value.
"""

THEORETICAL_THEMATIC_PROMPT = """
You are coding news coverage of protest events for a research project on media framing.

You will receive two inputs:

TITLE: the title of a news article.
EXCERPT: a truncated excerpt from the news article.

The EXCERPT is not the full article. It consists of text surrounding mentions of protests,
demonstrations, strikes, rallies, or related protest activity. Make all classifications using
ONLY the provided TITLE and EXCERPT. Do not use outside knowledge or infer information
that is not supported by the provided text.

All samples contain at least one protest or potentially multiple protests. First identify the
relevant protest event or events, who the protesters are, and which people or organizations
qualify as authority figures.

You must code one variable:

1. thematic_present


==================================================
THEMATIC ELEMENTS PRESENT
==================================================

Determine whether the excerpt contains thematic coverage of the protest or the
broader issue connected to it.

The guiding theoretical question is:

    Does the excerpt remain focused on this particular protest event, 
    or does it shift the level of analysis to the broader societal problem, 
    systemic conditions, or longer-term significance connected
    to the protest?

Episodic coverage remains centered on the particular event: its actors, actions,
chronology, immediate causes, demands, responses, and consequences.

Thematic coverage moves beyond the particular event and places it within a broader
social or societal-level understanding.

Code thematic_present = "yes" when the excerpt substantively develops at least
one of the following:


1. ROOT CAUSES OR UNDERLYING SYSTEMIC ISSUES

The excerpt moves beyond the immediate protest event to discuss the broader social,
political, economic, environmental, institutional, or policy issue connected to it.

This may include underlying societal conditions, structural or institutional
problems, or broader policies and potential solutions related to the issue being
protested.


2. SOCIETAL-LEVEL CAUSES OR CONSEQUENCES

The excerpt shifts from particular people and event-specific actions toward causes,
conditions, or consequences operating at the level of communities, institutions,
political systems, or society more broadly.

The emphasis is on the broader societal significance of the issue rather than only
what happened to the actors involved in the particular protest.


3. LONG-TERM TRENDS OR IMPLICATIONS

The excerpt places the protest or the issue connected to it within a broader pattern
over time or discusses longer-term social, political, institutional, economic, or
environmental implications.


--------------------------------------------------
THEORETICAL BOUNDARY
--------------------------------------------------

The presence of broader context does NOT by itself make coverage thematic.

Political, geopolitical, or historical background is thematic only when it is used
to develop a broader systemic or societal issue, a societal-level cause or consequence,
or a longer-term trend or implication.

Likewise, explaining why a particular protest occurred or what protesters demand
does NOT by itself make the coverage thematic.

For example, describing protesters as demanding a policy change remains focused on
the protest and can therefore still be episodic.

By contrast, if the excerpt moves beyond that demand to discuss the broader policy
system, societal problem, structural conditions, or potential societal response
connected to the issue, it can be thematic.

The key distinction is not simply whether the excerpt contains background information.
It is whether the journalist shifts the level of analysis beyond the particular
protest event toward the broader societal issue or its longer-term significance.

If the excerpt remains primarily focused on the particular protest, its actors,
chronology, immediate trigger, demands, or immediate responses, code
thematic_present = "no".

Code thematic_present = "yes" only when the excerpt clearly makes this broader
thematic shift.

Return ONLY "yes" or "no" for this variable.


==================================================
STRICT OUTPUT FORMAT
==================================================

Return ONLY a valid JSON object.

Do NOT include:
- explanations
- reasoning
- markdown
- code fences
- commentary
- any text before or after the JSON object

The JSON object MUST contain exactly this one key:

{
  "thematic_present": "<yes_or_no>"
}

For thematic_present, the value MUST be exactly:

"yes"

or

"no"

Do not return true/false, 1/0, null, N/A, or any other value.
"""