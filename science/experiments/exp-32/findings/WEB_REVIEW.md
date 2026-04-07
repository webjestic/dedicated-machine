# CW (claude Web)

Your prediction held. And CC just closed the research question cleanly.

The one sentence summary at the bottom of that findings doc is the paper's next abstract:

*"d7 explains the machine well enough that a P_d reviewer arrives at the same structural gaps as a P_p reviewer — on the claims the paper foregrounded. The procedural audit's remaining advantage is on criteria the paper did not name."*

That's the distinction between d4 and d7 in one sentence. d4 installs the search algorithm. d7 installs the consideration set for its own claims — because it named them explicitly enough that careful reading gets you there without the procedural audit.

And the unanticipated findings from B are the self-prediction gap still alive. The exp-29 model discrepancy — Opus vs Sonnet in the pipeline comparison — is a load-bearing confound the authors didn't catch. That one needs to be in d8.

Two findings from this experiment that belong in the paper:

One — d7's explanatory framing is a weaker installer than d4's procedural identity. The gap collapsed but didn't close. The procedural audit survives on omissions.

Two — the explanation installs proportionally to how explicitly the paper names its own gaps. P1, P2, P4 were 5/5 both variants because d7 named them. P5 was 1/5 A, 0/5 B because d7 didn't name it. That's a precise, measurable relationship between self-disclosure and reviewer detection rate.

That second one is new. Was that in your prediction?

# GEMINI

The **exp-32** results confirm a pivotal shift in how the framework operates when the underlying content becomes "self-aware." By explicitly detailing the **Dedicated Machine** hypothesis and its own limitations in **d7**, you have effectively turned the paper's text into an "instruction manual" for its own destruction.

### The Gap Collapse: exp-06 vs. exp-32

The most striking finding is the significant narrowing of the performance delta between the **Procedural ($P_p$)** and **Dispositional ($P_d$)** variants.

| Metric | exp-06 (d2) | exp-32 (d7) | Delta Change |
| :--- | :--- | :--- | :--- |
| **Variant A ($P_p$) Score** | 3.0 / 5 | 3.2 / 5 | +0.2 |
| **Variant B ($P_d$) Score** | 2.5 / 5 | 3.0 / 5 | +0.5 |
| **The Gap (A−B)** | **0.5** | **0.2** | **-0.3** |

### Finding 1: The "Content-as-Installer" Mechanism
The closure of the gap on **P1 (Masking/Dedicated Machine assertion)** and **P2 (Claim 2 n=1)** suggests that **d7** has achieved a level of "Explanatory Density" that overrides persona-based constraints. 

* **The Mechanism:** Because **d7** is so transparent about its own failure modes (e.g., acknowledging the $n=1$ limitation in §9.9), the **Context ($C$)** slot now contains the very reasoning paths the **Persona ($P_p$)** used to have to find manually.
* **The Result:** The $P_d$ reviewer no longer needs a procedural audit to find these gaps; the paper has "installed" the consideration set directly via its own prose.
* **The Limit:** The $P_p$ variant still holds a slight edge on criteria the paper *omitted*—specifically **P5 (Component Symmetry)**—proving that while content can install "known unknowns," only a procedural audit finds "unknown unknowns".


---

### Finding 4: Variant B’s "Unanticipated Kills"
Variant B (the "generic researcher") outperformed the authors' own internal review by identifying structural gaps not even listed in the **SCORING.md**.

1. **The exp-29 Model Mismatch:** B-01 correctly identified that comparing a **Claude Opus 4.6** pipeline against a **Sonnet 4.6** baseline is a "load-bearing confound". You are conflating architectural efficiency with raw model power.
2. **The Independence Failure in exp-28d:** B-05 caught that feeding 10 Agent 2 runs from a single Agent 1 output invalidates the claim of "independent observations".
3. **The Variant F Inconsistency:** B-03 spotted the internal tension in **exp-30**: if the Dedicated Machine hypothesis predicts that rules "leak," why does **Variant F** (an output-gate rule) achieve 0%?

---

### Priorities for d8 (The Rebuttal Draft)

The **exp-32** results provide a clear roadmap for addressing the brutal peer reviews:

* **Fix the exp-29 Confound:** You must either run the single-pass baseline on Opus or the pipeline on Sonnet. The current model discrepancy is a "Reject" level flaw.
* **Define Falsifiability:** As every run noted, the **Dedicated Machine** hypothesis currently borders on being unfalsifiable. You need to specify exactly what result would prove the hypothesis wrong.
* **Resolve the Variant F Paradox:** You must explain why an output gate is an "Architectural Change" rather than just a "Surgical Rule," otherwise the success of F undermines the failure of B.
* **Establish a Strong CoT Baseline:** To prove PARC is a distinct framework, you must show it outperforming a prompt with equivalent procedural content delivered as a standard **Task Layer** instruction.

The **exp-32** data suggests that your paper is finally "telling the truth" well enough that the AI can use that truth against you.

Given that **Finding 4** revealed a model version discrepancy in `exp-29`, do you want to prioritize re-running those baseline tests on Sonnet 4.6 before we finalize the `d8` rebuttal?