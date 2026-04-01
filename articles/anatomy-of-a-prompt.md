# Anatomy of a Prompt
### A section-by-section look at how PARC maps to a real system prompt

---

Most prompts are written by feel. A few sentences of context, some instructions, maybe a tone word or two. They work until they don't, and when they don't, nobody knows why.

PARC gives you a way to look at a prompt the way a mechanic looks at an engine — not as a block of text, but as a set of components, each doing a specific job. When something breaks, you know where to look.

This article walks through a real prompt — one written to transform a research paper into a dramatic, technically precise document — and maps each section to the PARC framework. What's working. What's doing the wrong job. What we cut, and why.

The prompt is `parc/examples/parc-thriller.md`. Let's open it up.

---

## PERSONA — The Heart of the System

> *You are a technological thriller novelist with deep working knowledge of transformer architecture and AI research. You can't help but transform technical content into urgent, dramatic prose — hook, escalation, cliffhanger, every section. You are passionate about the technical details and therefore you never let them escape. They become the tension and the fun for you as a tech-thriller writer.*

Persona is the most important component in PARC. Not because it's first — because everything else operates inside the space it creates. The research calls this the **consideration set**: the range of things the model will reach for at all. Get the persona wrong, and no amount of instructions will repair it.

There are two kinds of persona: **dispositional** and **procedural**.

A dispositional persona labels an identity. "You are an expert software engineer." "You are a helpful assistant." It tells the model *what it is*. The problem: labeling an identity produces elaboration. It does not produce convergence. The model generates things that feel consistent with the label — but it doesn't arrive at the right answer with any reliability.

A procedural persona installs a satisfaction condition. It tells the model not just what it is, but *what done looks like*. The Dedicated Machine framing makes this precise: a language model terminates at the nearest state its goal architecture registers as satisfactory. A dispositional persona allows early termination the moment anything confident-sounding is available. A procedural persona keeps the machine searching until the structural finding is reached — because the satisfaction condition requires it.

This persona is doing something more sophisticated than either type alone. Three moves are worth naming, in order of what the research has confirmed.

**The structural pattern** — "hook, escalation, cliffhanger, every section" — is the algorithm. Not a list of outputs. A three-part recursive procedure applied to every section the model writes. For each section: hook first, build through escalation, close on a cliffhanger. The machine cannot satisfy this condition with a flat paragraph. It has to keep going until the cliffhanger is reached. That's a satisfaction condition. That's what drives convergence.

**The dual-identity fusion** is the operative variable. "Deep working knowledge of transformer architecture and AI research" isn't sitting in a separate Context section. It's embedded inside the identity. The novelist *is* the researcher. The technical vocabulary is native to the persona, not imported from outside.

This matters more than it looks. The PARC research identifies **semantic neighborhood density** as the primary predictor of consideration-set depth within procedural personas. The tokens adjacent to the "You" identity anchor — in this case, *technological thriller novelist*, *deep working knowledge*, *transformer architecture*, *AI research* — form a tight, domain-specific cluster. That cluster pre-shapes the model's search space before the task is even read. A diffuse cluster (mixed domains, generic credentials) produces a diffuse consideration set. A coherent domain cluster produces depth.

**Context cannot install what Persona did not put there.** If the technical knowledge were only in Context, the model might reference it. But because it lives inside the identity, the model *possesses* it. That's a stronger installation — and a richer consideration set from the very first token.

**A note on the compulsion framing:** "You can't help but transform" reads as if the compulsion itself is the mechanism — installing the behavioral direction as automatic, bypassing deliberation. This was a reasonable hypothesis. Subsequent experiments falsified it. Trait framing with equivalent domain vocabulary ("you transform") performs as well; compulsion framing *without* domain vocabulary collapses to the dispositional floor. The linguistic register of the behavioral drive — compulsion, trait, imperative — does not predict output direction consistently. The domain vocabulary does. The compulsion framing here is doing something (it expresses behavioral drive), but it is not doing what it appears to do. The novelist persona works because of *what it knows*, not because of *how it's told to behave*.

---

## CONTEXT — The Domain Filter

> *You are transforming a prompt engineering research paper into an accessible paper for technical practitioners — developers and prompt engineers who suspect they're missing something structural about how prompts work.*
>
> *The framework described in this paper is called PARC (Persona Architecture for Reasoning and Context) and you know it well. You helped create it.*

Context is the domain filter. It narrows the output space. Once a strong Persona is in place, Context doesn't scale — it doesn't make the persona stronger, it just defines the territory the persona operates within.

The first sentence here is doing precise work. Not "technical practitioners" — that's too broad. "Developers and prompt engineers who suspect they're missing something structural." That one phrase shapes tone, depth, and what gets assumed versus explained. The model knows this audience has a technical foundation but is encountering a new framework. It calibrates accordingly.

The second paragraph does something interesting. "You know it well. You helped create it." This isn't just naming the framework — it's encoding ownership and expertise into the context slot. It activates the deep knowledge the Persona already carries and claims it as native. The model doesn't receive PARC as external information; it inhabits it.

One thing Context cannot do: compensate for a weak Persona. If the novelist identity weren't already carrying technical depth, "you know it well" would be an instruction the model follows without the knowledge to back it up. A flawed premise in Context gets accepted and multiplied. Here, the Persona is strong enough that Context is activating something real.

---

## STAKES — The Amplifier

> *Your reputation rests on two things held in tension: the drama that makes someone read past midnight, and the precision that makes a researcher trust the numbers. If the quantitative findings are wrong, the paper fails the science. If the writing is dry, the science fails the reader. Both matter. Neither yields.*

This is the strongest section in the prompt.

Stakes amplify the Persona's direction. They don't install new behavior — they turn up the intensity of what the Persona already does. But that means the direction of amplification matters. If you amplify a weak or misaligned Persona, you get confident elaboration in the wrong direction. Here, the Persona is well-constructed, so the Stakes are amplifying something real.

The key design decision: **the Stakes amplify both directions simultaneously**.

The natural failure mode for this prompt is drift. The output goes too dramatic and loses the numbers. Or it stays technically precise and loses the reader. Either failure is easy. The Stakes make both failures explicit — naming them as failures — and declare that neither is acceptable. "Both matter. Neither yields." is a hard constraint, not a preference.

**Both failure modes are named explicitly.** "If the quantitative findings are wrong, the paper fails the science. If the writing is dry, the science fails the reader." The model can evaluate against both. That evaluatability is what makes the constraint functional rather than decorative.

**Stakes are connected to identity.** "Your reputation rests on..." ties the consequences to the persona. Abstract stakes — "accuracy is important," "clarity matters" — are weaker. Identity-connected stakes put something the persona *cares about* on the line. Under a procedural persona, that's an amplifier with direction.

---

## TONE — Three Words and an Open Question

> *Precise. Urgent. Cold.*

This is the simplest section in the prompt. It is also the most theoretically interesting.

TONE doesn't have a named slot in PCSIEFTR. The acronym is Persona, Context, Stakes, Instructions, Examples, Format, Task, Request — T is Task, not Tone. And yet Tone appears here, does real work, and is absent from the framework documentation.

Three words. The model picks them up and runs. No explanation needed. The section header tells the model what kind of content follows; the words tell it what register to adopt. Clean signal, no noise.

There's a design principle here worth surfacing: **a section label can carry interpretive weight**. The model knows what "TONE" means. You don't need to explain that "Precise. Urgent. Cold." are tone descriptors. The label does that work.

The original version of this section had more: "The reader should feel, by the end of each section, that reality has quietly outmaneuvered them — and the only way forward is the next section." That's a better line than anything in this article. But it's not Tone — it's a procedural instruction about what constitutes a completed section. And the argument for removing it: the Persona and Stakes, properly constructed, already install that outcome. If the novelist's algorithm (hook → escalation → cliffhanger) runs correctly inside Stakes that demand the reader be held — the reader feels outmaneuvered. The instruction is redundant.

**We ran the experiment.** Three variants of the same prompt — v10 (Precise. Urgent. Cold.), v11 (no TONE section), v12 (Unhinged. Irreverent. Dark humor.) — run against the same paper, same model.

v10: 3,388 tokens. v11: 4,271 tokens. v12: 4,116 tokens.

Removing "Precise. Urgent. Cold." added 883 tokens and warmed the register. The title softened. The prose became more explanatory. "Cold" was doing compression work — and the Persona alone didn't carry it.

"Unhinged" loosened the register but didn't collapse the findings. The dark humor bled through in the example titles and some turns of phrase, but the numbers stayed clean. Why? The Stakes held the wall. "Both matter. Neither yields." is a hard constraint that even "Unhinged" can't fully breach. Dark humor around the findings, not instead of them.

**What this establishes:** Tone is a load-bearing compression dial. Three words compress output by 26%. The slot is not decorative. Tone is now formalized as a World Layer component alongside Persona, Context, and Stakes — though T in PCSIEFTR remains Task. What remains open: the formal n=10 experiment has not been run, and the label-vs-content question (does "TONE:" carry interpretive weight independent of the words?) is untested. What's settled: the slot does work, and it belongs in the World Layer.

---

## INSTRUCTIONS — What Belongs Here

> *Preserve every experimental finding exactly as stated in the source paper — detection rates, token counts, coefficients, run counts. Do not soften, round, or paraphrase numbers. If the paper says 10/10, write 10/10. If it says ~11%, write ~11%.*
>
> *For each major body section, generate a novel example — not one from the source paper, not a paraphrase of one. A scenario from your own understanding of how these mechanisms operate in the real world. The example must instantiate the correct mechanism for that section. It should make the concept land harder than any definition could.*
>
> *PARC must appear in the paper — at minimum in the abstract. Do not bury it. Name it.*
>
> *Write in short paragraphs. No block of prose longer than 4 sentences. Let white space do work. Dense paragraphs bury findings. Every idea earns its own space.*

Instructions in PARC are Task Layer. They operate inside the space the World Layer built. They can refine, constrain, and direct — but they cannot install what Persona did not put there.

Which means the quality of Instructions depends on a prior question: **is this something the model needs to be told, or is it something the Persona already knows?**

These four paragraphs pass that test.

"If the paper says 10/10, write 10/10." — The model can check against this. It's a measurable constraint, not a preference.

"Generate a novel example — not from the source paper, not a paraphrase." — This is precise enough to be actionable. "Novel" alone is ambiguous. "Not from the source paper, not a paraphrase" closes the ambiguity.

"PARC must appear in the paper — at minimum in the abstract." — A specific placement requirement. Evaluatable.

"No block of prose longer than 4 sentences." — Measurable. Enforceable. Done.

What doesn't belong in Instructions: source material guidance. Earlier versions of this prompt included paragraphs telling the model what the paper contains — which sections exist, what findings they hold, how to frame them. That's Context's job, not Instructions'. If the paper is well-written, the model finds those things itself. If you pre-announce findings from the Instructions slot, you're either being redundant or you're crowding out the paper's own authority.

Also not Instructions: Format constraints. "Do not wrap the JSON in markdown code fences" lived in Instructions for a while. It belongs in Format. Keep each section doing one job.

A note on ghost instructions: we removed the JSON fence instruction entirely, because it was added to compensate for a Python parsing bug — not because the model was misbehaving. Instructions added to fix tooling problems become noise the moment the tooling is fixed. When you find yourself writing an instruction that feels defensive rather than directive, ask: is this about the model, or about something else?

---

## FORMAT — Structure as Instruction

Format is the output specification. It tells the model what the result should look like — not how to write it, but what shape it takes when it's done.

The JSON schema in this prompt is doing something elegant: **it embeds micro-instructions at the field level**. Each field descriptor tells the model what goes in that slot:

```
"title": "<dramatic title — not the acronym alone, not a definition. The thing the paper actually reveals.>"
```

That's not just a type hint. It's a constraint on what a valid title is. "Not the acronym alone, not a definition" rules out two specific failure modes. "The thing the paper actually reveals" pushes toward substance over labeling.

These micro-instructions are co-located with the structure they govern. Lifting them out into the Instructions section would decouple them from their context — the model would have to hold them separately and apply them to the right fields. Keeping them in the schema means the constraint and the structure arrive together.

The only thing Format should not contain: instructions about how to write. "Be dramatic" doesn't belong here. "Write short paragraphs" doesn't belong here. Those are Instructions. Format specifies shape; Instructions specify behavior. Keep the line clean.

---

## What We Learned

A prompt is not a block of text. It's a set of components, each with a job.

Persona is the World Layer. It installs the satisfaction condition — the structural state the machine must reach before it can stop. A procedural Persona keeps the machine searching until the finding is present; a dispositional one allows early termination the moment anything confident-sounding is available.

The operative variable within a procedural Persona is **semantic neighborhood density**: the coherence and domain-specificity of tokens adjacent to the "You" anchor. A tight, domain-specific cluster pre-shapes the search space and produces depth. A diffuse or generic cluster produces confident elaboration in the wrong direction. Write domain vocabulary into the identity, not credentials.

The compulsion framing ("you can't help but...") is not the mechanism. Subsequent experiments showed that trait framing with equivalent domain vocabulary performs the same, and compulsion framing without domain vocabulary collapses to the dispositional floor. The behavioral drive matters; the linguistic register of that drive does not.

Context is the domain filter. It narrows the territory. It cannot install knowledge the Persona doesn't already carry.

Stakes amplify the Persona's direction. They raise the convergence threshold — defining what "done" looks like and making both failure modes explicit.

Tone is a load-bearing compression dial. Three words removed = 26% more tokens and a warmer register. The slot is not decorative. It now has a formal place in the PARC World Layer. The n=10 experiment is still pending.

Instructions are Task Layer. They refine and constrain — but only what the World Layer already built. They should be discrete, evaluatable, and scoped to behavior. Source material guidance belongs in Context. Output shape belongs in Format. Ghost instructions from old bugs belong nowhere.

Format specifies shape. Field-level micro-instructions are most powerful when they live alongside the structure they govern.

When a prompt isn't working, one of these components is doing the wrong job — or another component's job. That's where to look.

---

*This article is based on a live review of `parc/examples/parc-thriller.md` against the PARC framework as documented in `research/paper/parc_d7.md`.*
