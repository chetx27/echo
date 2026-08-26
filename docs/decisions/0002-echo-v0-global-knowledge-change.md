# Decision: ECHO V0 is global expected knowledge change

**Decision:** ECHO V0's acquisition score is the expected reduction in posterior entropy of the latent function on a domain probe set. It is not a weighted sum of uncertainty, EI, and other terms.

**Reason:** Every term in an acquisition function needs a scientific interpretation. "Expected change in global scientific belief" is one quantity. Arbitrary weights would be a method that cannot be defended.

**Alternatives:** Local BALD, EI, a linear combination of scores, a learned acquisition.

**Rejected because:** Local BALD is already the `information_gain` baseline. EI is already a baseline. Weighted sums without a utility derivation are not V0. Learned acquisition is a later question.

**Consequences:** The mathematics overlaps GP mutual-information design (MacKay 1992; Krause et al. 2008). The research claim, if any, cannot be "we invented information gain." It can only be about whether this objective tracks discovery metrics in the ECHO evaluation protocol.
