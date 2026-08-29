# Chandola, V., Banerjee, A., & Kumar, V. (2009)

- **Citation:** Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly detection: A survey. *ACM Computing Surveys*, 41(3), Article 15.
- **Year:** 2009
- **Problem:** Detect unusual points or regions relative to a background model.
- **Method:** Survey of classification, nearest-neighbor, clustering, statistical, and spectral approaches.
- **Dataset/environment:** Broad; the note is used for problem framing, not a single dataset.
- **Objective:** Flag anomalies. Not sequential scientific design.
- **Baseline:** Many; survey paper.
- **Limitations:** Detection is not the same as concluding that a scientific model is incomplete.
- **Relevance to ECHO:** The anomaly world hides a structured local violation of an otherwise simple law. The evaluation target is whether sequential design *finds* that region, not whether a one-shot detector would flag it given the whole dataset.
- **Potential research gap:** Whether uncertainty sampling over-explores high-variance noise and misses a compact, structured deviation.
