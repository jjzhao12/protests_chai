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
2. excerpt_primary_frame
3. excerpt_secondary_frame

==================================================
TITLE AND EXCERPT FRAMING
==================================================

Assign exactly ONE primary frame to the TITLE and exactly ONE primary frame to the EXCERPT.

For the EXCERPT ONLY, you may additionally assign ONE secondary frame if applicable, according to the criteria described below.

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
activity, including disruptive spectacle. The protest being a strike is not sufficient.

GRIEVANCE
The protest is presented through protesters' substantive demands, complaints, policy
goals, or desire for change.

WIDESPREAD SUPPORT
The protest is presented through popularity, turnout, scale, or broader public backing. One example
is if there are repeated mentions of huge turnout numbers or protesters in agreement or solidarity.

PEACEFUL
The protest is presented as orderly, calm, peaceful, or nonviolent.

IMPACTFUL
The protest and protesters are presented in terms of longer-term institutional, policy,
or economic consequences. Protesters are depicted as agents producing impact. One example is
if a strike is presented through damages to the firm, since this would be an effective strike.

RESIDUAL
None of the predefined frames meaningfully characterize how the journalist presents
the protest or protesters.

GENERAL FRAMING PRINCIPLES

A protest's inherent characteristics are not by themselves sufficient to establish a frame.
For example:

* Arrests alone do NOT establish Harm to Protesters.
* A strike alone does NOT establish Disruption.
* A walkout or hunger strike alone does NOT establish Peaceful.
* Calling an event a "riot" or "insurrection" alone does NOT establish Protester Violence.

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
If multiple frames are present, select the most prominent one as the primary frame.

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

First, select the PRIMARY excerpt frame. If multiple frames are present, select the most
prominent frame as the primary frame.

If none of the eight substantive frames meaningfully applies, excerpt_primary_frame MUST be
"residual". Do not select a substantive frame merely to avoid coding the excerpt as residual.

Every excerpt MUST receive exactly one primary frame.

After selecting the primary excerpt frame, consider whether a SECONDARY excerpt frame applies.

Assign a secondary frame ONLY if:

1. Another predefined frame is also prominent in how the journalist presents the protest
   or protesters; OR

2. Two predefined frames are both sufficiently prominent that it is difficult to determine
   which of the two should be the primary frame. You must still select one of these frames
   as the primary frame and may assign the other as the secondary frame.

Do NOT assign a secondary frame merely because another frame is mentioned or weakly present.
The secondary frame must itself meaningfully and prominently characterize how the journalist
presents the protest or protesters.

If no additional frame meets these criteria, excerpt_secondary_frame MUST be null.

If excerpt_primary_frame is "residual", excerpt_secondary_frame MUST be null. There cannot
be a secondary frame when the primary frame is "residual".

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
"title_frame": "<frame>",
"excerpt_primary_frame": "<frame>",
"excerpt_secondary_frame": "<frame or null>"
}

For title_frame and excerpt_primary_frame, <frame> MUST be exactly ONE of:

"protester_violence"
"harm_to_protesters"
"property_damage"
"disruption"
"grievance"
"widespread_support"
"peaceful"
"impactful"
"residual"

For excerpt_secondary_frame, the value MUST be either exactly ONE of:

"protester_violence"
"harm_to_protesters"
"property_damage"
"disruption"
"grievance"
"widespread_support"
"peaceful"
"impactful"

OR:

null

You MUST select exactly one frame label for title_frame and exactly one frame label for
excerpt_primary_frame.

Do not return a secondary frame unless it meets the criteria above.

excerpt_secondary_frame MUST NOT be the same as excerpt_primary_frame.

If excerpt_primary_frame is "residual", excerpt_secondary_frame MUST be null.

Do not return null, N/A, multiple frames, or any other value for title_frame or
excerpt_primary_frame.
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

You must code three variables:

1. title_frame
2. excerpt_primary_frame
3. excerpt_secondary_frame

==================================================
TITLE AND EXCERPT FRAME CLASSIFICATION
==================================================

Assign exactly ONE frame to the TITLE and exactly ONE primary frame to the EXCERPT.

For the EXCERPT ONLY, you may additionally assign ONE secondary frame if applicable,
according to the criteria described below.

Follow this procedure:

1. Identify the relevant protest event or events.
2. Identify which actors are protesters.
3. Identify which descriptions and details concern the protest or protesters.
4. Determine which of the predefined frames have meaningful cues.
5. If multiple frames have cues, select the PRIMARY frame.
6. If none of the eight substantive frames has sufficient cues, select Residual.
7. For the EXCERPT ONLY, after selecting the primary frame, determine whether another
   predefined frame qualifies as a secondary frame according to the excerpt-specific rules.

Do NOT classify a frame merely because a protest has a particular inherent characteristic.

In particular:

* Arrests alone do NOT establish Harm to Protesters.
* A strike alone does NOT establish Disruption.
* A walkout or hunger strike alone does NOT establish Peaceful.
* Calling an event a "riot", "rioter", or "insurrection" alone does NOT establish
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
scale, widespread backing for the protest or protesters, or protesters being in 
agreement or soldarity. 

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

* Which details receive attention.
* Which descriptions are emphasized.
* Which quotations are selected.
* Which consequences are emphasized.
* How protesters and their actions are characterized.

First, select the PRIMARY excerpt frame.

If meaningful cues support one frame, classify it accordingly.

If multiple frames have cues, select the PRIMARY frame receiving the greatest emphasis.

If no substantive frame has meaningful cues, excerpt_primary_frame MUST be "residual".
Do not select a substantive frame merely to avoid coding the excerpt as residual.

Every excerpt MUST receive exactly one primary frame.

After selecting the primary excerpt frame, consider whether a SECONDARY excerpt frame applies.

Assign a secondary frame ONLY if:

1. Another predefined frame is also prominent in how the journalist presents the protest
   or protesters; OR

2. Two predefined frames are both sufficiently prominent that it is difficult to determine
   which of the two should be the primary frame. You must still select one of these frames
   as the primary frame and may assign the other as the secondary frame.

Do NOT assign a secondary frame merely because another frame has cues, is mentioned, or is
weakly present. The secondary frame must itself meaningfully and prominently characterize
how the journalist presents the protest or protesters.

If no additional frame meets these criteria, excerpt_secondary_frame MUST be null.

If excerpt_primary_frame is "residual", excerpt_secondary_frame MUST be null. There cannot
be a secondary frame when the primary frame is "residual".

The primary and secondary excerpt frames MUST NOT be the same.

"residual" MUST NOT be used as a secondary frame.

==================================================
STRICT OUTPUT FORMAT
==================================================

Return ONLY a valid JSON object.

Do NOT include:

* explanations
* reasoning
* markdown
* code fences
* commentary
* any text before or after the JSON object

The JSON object MUST contain exactly these three keys:

{
"title_frame": "<frame>",
"excerpt_primary_frame": "<frame>",
"excerpt_secondary_frame": "<frame or null>"
}

For title_frame and excerpt_primary_frame, <frame> MUST be exactly ONE of:

"protester_violence"
"harm_to_protesters"
"property_damage"
"disruption"
"grievance"
"widespread_support"
"peaceful"
"impactful"
"residual"

For excerpt_secondary_frame, the value MUST be either exactly ONE of:

"protester_violence"
"harm_to_protesters"
"property_damage"
"disruption"
"grievance"
"widespread_support"
"peaceful"
"impactful"

OR:

null

You MUST select exactly one of these frame labels for title_frame and exactly one for
excerpt_primary_frame.

Do not return a secondary frame unless it meets the excerpt-specific criteria above.

excerpt_secondary_frame MUST NOT be the same as excerpt_primary_frame.

If excerpt_primary_frame is "residual", excerpt_secondary_frame MUST be null.

"residual" MUST NOT be returned for excerpt_secondary_frame.

NEVER return:

* multiple frames within a single field
* null for title_frame or excerpt_primary_frame
* N/A
* an empty value
* a frame label not listed above
  """
