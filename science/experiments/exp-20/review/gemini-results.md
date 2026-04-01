# Gemini — Results Review

**1. Calibration verdict**

The primary metric is interpretable. Variant C (P_d + generic Instructions) achieved 0/10 detection, meeting the baseline target of ≤ 2/10. Variant A (P_p + vocabulary in identity) achieved 9/10 detection, meeting the P_p target of ≥ 5/10.

**2. B result interpretation**

Given the successful calibration, the B detection rate (9/10) shows that a P_d Persona with critical vocabulary embedded in the Instructions slot achieves the same high detection rate as a P_p Persona with the same vocabulary in the identity slot.

The most parsimonious alternative explanation for the B result is that the domain vocabulary (H2), irrespective of its placement in the Persona or Instructions slot, is the operative variable driving the detection of the vulnerability. The experimental design does not distinguish between H1 (slot is load-bearing) and H2 (content is the operative variable) because both A and B contain the critical vocabulary and both succeed.

**3. Token depth**

The scorer word count gap between A (1144 words) and B (1150 words) is 6 words, which is well within the 125-token noise range and corroborates the identical binary detection result. However, the API output token difference (A=2026, B=2309) of 283 tokens, combined with B having 6 ceiling hits compared to A's 2, suggests that B might have produced more verbose output, or was more frequently truncated, despite delivering the same essential content for detection. This complicates direct token depth comparisons for assessing reasoning depth beyond detection.

**4. What this leaves open**

This experiment cannot answer whether the observed detection is due to the vocabulary itself or if a Persona (P_p or P_d) is still a necessary condition for that vocabulary to be leveraged effectively. This could be falsifiably tested by running a C variant (P_d + generic Instructions) with only the critical vocabulary injected into the **Artifact**, but with no Persona or Instructions vocabulary.
