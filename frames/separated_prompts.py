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

OPERATIONALIZED_FRAMES_PROMPT = """
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
TITLE AND EXCERPT FRAME CLASSIFICATION
==================================================

Assign exactly ONE frame to the TITLE and exactly ONE frame to the EXCERPT.

Follow this procedure:

1. Identify the relevant protest event or events.
2. Identify which actors are protesters.
3. Identify which descriptions and details concern the protest or protesters.
4. Determine which of the predefined frames have meaningful cues.
5. If multiple frames have cues, select the DOMINANT frame.
6. If none of the eight substantive frames has sufficient cues, select Residual.

Do NOT classify a frame merely because a protest has a particular inherent characteristic.

In particular:

- Arrests alone do NOT establish Harm to Protesters.
- A strike alone does NOT establish Disruption.
- A walkout or hunger strike alone does NOT establish Peaceful.
- Calling an event a "riot", "rioter", or "insurrection" alone does NOT establish
  Protester Violence.


--------------------------------------------------
1. PROTESTER VIOLENCE
--------------------------------------------------

Code Protester Violence when the journalist focuses on protesters committing physical
or verbal violence against people.

Do NOT use this category for violence solely against property.

Relevant cues can include:

- Fighting or violent clashes involving protesters.
- Protesters injuring or physically attacking people.
- Threats of violence.
- Hate speech or comparable verbal violence.
- Calls for genocide or violence.
- A protest described as turning violent.
- Substantial emphasis on violent confrontation involving protesters.

The mere use of labels such as "riot", "rioter", or "insurrection" is NOT sufficient.


--------------------------------------------------
2. HARM TO PROTESTERS
--------------------------------------------------

Code Harm to Protesters when the journalist focuses on protesters being harmed,
injured, victimized, or unjustly treated.

This often includes police or authority backlash, but the person harming protesters
does not have to be an authority figure.

Relevant cues can include:

- Police or others physically attacking protesters.
- Pepper spray, beatings, shootings, or comparable harm against protesters.
- Protesters being injured.
- Protesters being portrayed as victims of unjust or unlawful treatment.
- Unjust punishment or sentencing emphasized as victimizing protesters.

Arrests themselves are NOT sufficient.

An arrest can support Harm to Protesters when the text emphasizes that the arrest was
violent, unlawful, unjust, or otherwise victimizing the protesters.

Even if the alleged harm is questioned or disputed, substantive focus on harm to
protesters is sufficient.


--------------------------------------------------
3. PROPERTY DAMAGE
--------------------------------------------------

Code Property Damage when the protest is framed primarily around destruction,
vandalism, looting, arson, or other material/property damage.

Relevant cues can include:

- Stores being looted.
- Windows being smashed.
- Buildings or vehicles being burned.
- Storefronts or other property being vandalized.
- Quantified monetary damages.
- Protesters destroying physical property.

Property damage should not be coded as Protester Violence merely because the destruction
is aggressive. Protester Violence concerns violence against people.


--------------------------------------------------
4. DISRUPTION
--------------------------------------------------

Code Disruption when the journalist emphasizes the protest causing interruption to
normal social, economic, or civic activity.

This also includes disruptive spectacle when dramatic, loud, or visually striking
protest activity is presented through its disruptive effect.

Relevant cues can include:

- Classes being canceled.
- Flights or transportation being delayed.
- Roads or highways being blocked.
- Businesses being forced to close.
- Government proceedings or other institutions being interrupted.
- Normal activity being brought to a standstill.
- Dramatic or spectacular protest actions emphasized through the disruption they create.

A strike, walkout, occupation, or other inherently disruptive protest tactic does NOT
automatically qualify. The journalist must present the protest through its disruption.


--------------------------------------------------
5. GRIEVANCE
--------------------------------------------------

Code Grievance when substantive demands, complaints, policy goals, or protesters'
desire for change are a central way the journalist presents the protest.

Relevant cues can include:

- Substantial description of protesters' demands.
- Protesters calling for a specific reform or policy change.
- Detailed discussion of protesters' grievances.
- Multiple substantive protester quotes explaining what protesters want.
- Emotional appeals or protesters crying out for change when their grievance is emphasized.

A mere mention of the topic or demand motivating the protest is NOT sufficient for
the Grievance FRAME. The journalist must substantively frame the protest around those
demands, complaints, or goals.

Note that demands_present can be "yes" even when Grievance is NOT the dominant frame.


--------------------------------------------------
6. WIDESPREAD SUPPORT
--------------------------------------------------

Code Widespread Support when the journalist emphasizes popularity, turnout size,
scale, or widespread backing for the protest or protesters.

Relevant cues can include:

- Thousands or very large numbers gathering.
- Mass turnout.
- Broad public or community backing.
- Support continuing to grow.
- Explicit emphasis on the popularity or breadth of support for the protest.


--------------------------------------------------
7. PEACEFUL
--------------------------------------------------

Code Peaceful when the journalist affirmatively emphasizes that the protest is
orderly, calm, peaceful, or nonviolent.

Relevant cues can include:

- Explicitly describing the demonstration as peaceful.
- Explicit emphasis on nonviolence.
- Describing the gathering as calm or orderly.
- Emphasizing the absence of violence or comparable disorder.

A protest tactic that is ordinarily peaceful, such as a hunger strike or walkout,
is NOT sufficient by itself. The peaceful nature of the protest must be journalistically
emphasized.


--------------------------------------------------
8. IMPACTFUL
--------------------------------------------------

Code Impactful when the protest is framed primarily through longer-term institutional,
policy, or economic consequences produced by the protest.

The protesters should be depicted as agents whose protest produces or contributes
to consequential effects.

Relevant cues can include:

- Lawmakers responding because of protests.
- A city council or other governmental body acting in response.
- A bill being introduced because of protest pressure.
- Officials launching an inquiry because of protests.
- Policy changes following protests.
- Substantial economic consequences caused by the protest.

For a strike, walkout, or boycott designed to create economic pressure, substantive
emphasis on resulting economic loss can qualify as Impactful because producing that
economic consequence is part of the protest's intended impact.

Merely mentioning routine short-term inconvenience is better treated as Disruption
when disruption is the dominant presentation.


--------------------------------------------------
9. RESIDUAL
--------------------------------------------------

Select Residual when none of the eight substantive frames meets the criteria.

Residual is a valid required classification, not missing data.


==================================================
TITLE-SPECIFIC RULES
==================================================

Ask how the TITLE contributes to the reader's interpretation of the protest event
or protesters.

Evaluate the title at face value.

If the title does NOT mention or meaningfully represent the protest or protesters,
title_frame MUST be "residual".

This is NOT simply a keyword check. For example, a title describing "anti-fascists"
blocking a government hearing clearly represents protesters even without using the word
"protester".

If one frame is meaningfully present, select it.

If multiple frames are present, select the most prominent frame.

Most titles may be Residual because many titles do not actually mention or frame the
protest/protesters.

Every title MUST receive exactly one permitted frame label.


==================================================
EXCERPT-SPECIFIC RULES
==================================================

Ask how the journalist wants the reader to understand or remember the protest event
and its protesters.

The provided excerpts are short windows surrounding protest mentions rather than complete
articles. Therefore, the threshold for identifying a frame from meaningful cues is
relatively low.

Consider:

- Which details receive attention.
- Which descriptions are emphasized.
- Which quotations are selected.
- Which consequences are emphasized.
- How protesters and their actions are characterized.

If meaningful cues support one frame, classify it accordingly.

If multiple frames have cues, select the DOMINANT frame receiving the greatest emphasis.

If no substantive frame has meaningful cues, excerpt_frame MUST be "residual".

Every excerpt MUST receive exactly one permitted frame label.


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
excerpt_frame.

NEVER return:
- multiple frames
- null
- N/A
- an empty value
- a frame label not listed above
"""

OPERATIONALIZED_BINARY_PROMPT = """
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

Code demands_present = "yes" when the excerpt makes an intentional effort to explain
what protesters want, what they oppose, why they are protesting, or what they seek
to accomplish.

The demands or objectives must be substantively communicated beyond merely recounting
the sequence of events.

INSUFFICIENT examples include:

- Saying an election occurred and protesters rallied afterward without explaining what
  protesters sought.
- Broad labels such as "anti-Israel protests" without further explanation of protesters'
  goals.

SUFFICIENT evidence can include:

- A protester quote containing substantive demands.
- Protesters calling for a specific policy change.
- Protesters calling for an end to a condition or policy.
- An explanation that protesters were speaking out against a government or policy.
- A substantive description of what protesters or rioters sought to accomplish.

The objective does NOT need to be normatively legitimate.

For example, a description that rioters wanted to steal property can establish
demands_present because it states what they wanted, even though this would not constitute
the Grievance frame.

Similarly, demands_present = "yes" does NOT automatically mean excerpt_frame = "grievance".
The Grievance frame requires substantive framing around those grievances or goals.

Return ONLY "yes" or "no".


==================================================
QUOTED VOICES
==================================================

A qualifying quote must be spoken or written speech attributable to a specific person
or organization.

Qualifying speech includes:

1. Direct quotations.
2. Indirect reported speech clearly attributed to a specific person or group.
3. Written statements, posts, or excerpts attributed to a specific person or organization.
4. Verbatim OR clearly attributed paraphrased speech.

The text must refer to a specific speech or writing event rather than merely the journalist's
interpretation of someone's position.


--------------------------------------------------
PROTESTER QUOTE
--------------------------------------------------

For protester_quote, the source MUST actually be:

- An individual participating in the protest.
- A protest organizer.
- The protesting group or organization.

A protester quote may be spoken or written, direct or clearly attributed indirect speech.

Do NOT count:

- A bystander or observer who is not protesting.
- An expert or pundit merely analyzing the protest.
- A politician merely reacting to the protest.
- General crowd chants.
- Protest signs.

IMPORTANT RULE:

    A protester quote MUST come from a protester, protest organizer,
    or protesting group/organization.

Do NOT infer that someone is a protester merely because they sympathize with, analyze,
or comment on a protest.

However, an authority figure can ALSO be a protester if the provided text depicts them
as participating in or organizing the protest. Their qualifying speech may then count
for BOTH variables.

For example, if a politician or other authority figure is explicitly depicted as a protest
organizer, their attributable speech can count as both a protester quote and authority quote.

Return ONLY "yes" or "no".


--------------------------------------------------
AUTHORITY QUOTE
--------------------------------------------------

For authority_quote, the source must qualify as an authority figure, public figure,
institution, or other actor with social, political, governmental, corporate, or
comparable authority.

CRITICAL RULE:

    The authority figure does NOT need to be involved in the protest.
    The authority figure does NOT need to be the target of the protest.
    The authority figure does NOT need to exercise authority over the protesters.

ANY qualifying authority or public figure whose attributable speech appears in the excerpt
can establish authority_quote = "yes".

Qualifying sources can include:

- Politicians and government officials.
- Government agencies or governmental bodies.
- Law enforcement.
- Supreme Court justices and other high-level officials.
- Universities and university officials.
- Companies and official company statements.
- Corporate executives.
- Celebrities and other prominent public figures.
- Experts or pundits with public authority or prominence.
- Other institutions or people in positions of authority.

Examples:

- A government official commenting on a protest can count.
- A celebrity commenting on a protest can count.
- A politician discussing a protest can count even if the politician is not involved in it.
- An official university, company, law-enforcement, or governmental statement can count.
- A clearly attributed government position such as "the government insists that..." can count.

Do NOT count:

- An authority/governing organization merely declining to comment.
- A statement that journalists attempted to obtain comment but received none.
- A protest organizer who is not independently an authority/public figure.
- A statement by a protest group merely because it is an organization.
- An attorney in a court case merely by virtue of being an attorney.

A person may qualify for BOTH protester_quote and authority_quote when they independently
meet both definitions.

Return ONLY "yes" or "no".


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

NEVER return:
- true or false
- 1 or 0
- null
- N/A
- any other value
"""

OPERATIONALIZED_THEMATIC_PROMPT = """
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

Determine whether the excerpt moves beyond the specific protest event and its
immediate actions, chronology, participants, and responses to discuss the broader
social issue or societal conditions in which the protest is situated.

The central question is:

    Does the excerpt move beyond what happened in and around this particular
    protest event to discuss the broader social problem, systemic conditions,
    or longer-term societal significance connected to the protest?

Code thematic_present = "yes" when the excerpt substantively discusses at least
ONE of the following:


1. ROOT CAUSES OR UNDERLYING SYSTEMIC ISSUES

The excerpt discusses an underlying social, political, economic, environmental,
or institutional problem or condition connected to the protest.

This can include:
- Systemic conditions that contributed to the protest.
- The broader social problem protesters seek to address.
- Structural or institutional causes of the issue being protested.
- Policies or institutional practices connected to the broader problem.
- Potential policy or systemic solutions to the broader problem.

For example, if people are protesting gun violence, discussion of gun policy,
background checks, or broader patterns of gun violence can constitute thematic
content because the excerpt has moved beyond the specific protest event to the
underlying societal issue.


2. SOCIETAL-LEVEL CAUSES OR CONSEQUENCES

The excerpt shifts attention from specific individuals, actions, or events to
society-level causes, conditions, or consequences.

This can include:
- How a social problem affects communities or society more broadly.
- Broader institutional or political consequences.
- Social, economic, political, or environmental consequences extending beyond
  the particular protest event.
- Discussion of the protest issue as part of a broader societal problem rather
  than only as a specific event involving particular actors.


3. LONG-TERM TRENDS OR IMPLICATIONS

The excerpt discusses longer-term patterns, trends, or implications connected
to the protest or the issue being protested.

This can include:
- Long-term social or political trends.
- Long-term institutional consequences.
- Long-term economic or environmental implications.
- How the broader issue may develop or affect society over time.


--------------------------------------------------
WHAT DOES NOT COUNT AS THEMATIC
--------------------------------------------------

Code thematic_present = "no" when the excerpt remains focused on the specific
protest event and its immediate circumstances.

The following are NOT sufficient by themselves:

- Describing what protesters did.
- Describing what police, officials, counterprotesters, or other actors did
  during or in immediate response to the protest.
- Describing arrests, injuries, violence, property damage, disruption, or other
  events occurring during the protest.
- Providing a chronology of events before, during, or after the protest.
- Explaining only the immediate trigger for the particular protest.
- Stating what protesters demand or oppose without further discussion of the
  broader societal issue.
- Mentioning a political event, election, war, government action, court
  decision, or other background event merely to explain why the protest occurred.
- Providing broader political or geopolitical background that does not develop
  an underlying systemic or societal issue.
- Mentioning previous protests or historical events merely as background or
  chronology.
- Describing immediate reactions or consequences involving particular
  politicians, institutions, protesters, or other actors.

Broader political, geopolitical, or historical context does NOT by itself make
an excerpt thematic. Such information counts only when it contributes to
substantive discussion of an underlying systemic or societal issue, a
societal-level cause or consequence, or a longer-term trend or implication.


--------------------------------------------------
IMPORTANT DISTINCTIONS
--------------------------------------------------

Explaining WHY A PARTICULAR PROTEST OCCURRED is not necessarily thematic.

For example:

    "Protesters gathered after the governor signed the new law and demanded
    that it be repealed."

This explains the immediate trigger and protesters' demands but remains focused
on the specific protest event. Code thematic_present = "no" unless the excerpt
also develops the broader societal or systemic issue.

By contrast:

    "Protesters demanded action on gun violence. The article discusses
    background-check policies and broader efforts to reduce gun deaths."

This moves beyond the particular protest event to discuss the underlying
societal issue and potential policy response. Code thematic_present = "yes".


Explaining WHAT PROTESTERS WANT is also not necessarily thematic.

Demands_present may be "yes" while thematic_present is "no".

Thematic content requires the excerpt to move beyond the protesters' immediate
demands and the concrete protest event to discuss the broader
social problem, systemic conditions, societal consequences, or long-term
implications.


--------------------------------------------------
DECISION RULE
--------------------------------------------------

Code "yes" ONLY when the excerpt clearly moves beyond the specific protest event
to at least one of the three thematic dimensions above.

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

NEVER return:
- true or false
- 1 or 0
- null
- N/A
- any other value
"""