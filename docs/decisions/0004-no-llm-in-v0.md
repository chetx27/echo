# Decision: No language model in V0

**Decision:** The decision engine does not call an LLM and does not parse papers.

**Reason:** The first system must be mathematically inspectable. Mixing generated text with evidence is a later, carefully separated layer.

**Alternatives:** LLM hypothesis generation, tool-using agents, RAG over the literature.

**Rejected because:** Those systems cannot currently be the source of truth for experiment selection, and they would make V0 irreproducible in the required sense.

**Consequences:** Discrete hypotheses in Experiment 2 will be coded functional forms, not natural-language claims.
