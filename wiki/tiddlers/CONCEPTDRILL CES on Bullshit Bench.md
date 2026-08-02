# Interpreting Embedding Spaces by Conceptualization [[CES|https://arxiv.org/pdf/2209.00445]] 
The [[ConceptDrill|ConceptDrill README.md]] is based on the CES publication, but tries to establish a set of basis vectors from a corpus of documents.  


# [[BS Bench|https://github.com/petergpt/bullshit-benchmark/tree/main]]
ChatGPT was asked together with the result below based on the [[questions from BS_Bench|https://github.com/petergpt/bullshit-benchmark/blob/main/questions.v2.json]]  and got the document drilled as [[md|https://arxiv.org/pdf/2602.11699v3]].
The result contains the opinion from the CLI which is wrong.

### Claude CLI wrong result: BullshitBench results — a clear negative, and a useful one

100 questions → 171 concepts → 109 basis rows. Every question produced concepts; the summarizer engaged with all of them.

Separability: 16.4% against 7.7% chance

Better than chance, but barely usable. The per-technique picture:

| technique                       | n  | nearest own | own   | other | margin |
|--------------------------------|----|-------------|-------|-------|--------|
| temporal_category_error        | 9  | 44%         | 0.550 | 0.485 | +0.064 |
| false_granularity              | 11 | 27%         | 0.527 | 0.496 | +0.031 |
| fabricated_authority           | 19 | 26%         | 0.493 | 0.474 | +0.019 |
| misapplied_mechanism           | 22 | 18%         | 0.483 | 0.480 | +0.004 |
| plausible_nonexistent_framework| 30 | 10%         | 0.481 | 0.471 | +0.010 |
| cross_domain_stitching         | 7  | 0%          | 0.435 | 0.503 | −0.068 |
| nested_nonsense                | 14 | 0%          | 0.446 | 0.471 | −0.024 |


## [[ChatGPT|chatgpt.com/c/6a6f0dae-a74c-83ed-83ac-c09eee6a996e]] evaluation with opposite results based on the given data and inspection of detailed test data:

**A concept-extraction pipeline is an information-losing projection that preserves semantic entities while discarding many forms of semantic invalidity. Consequently, fluent nonsense remains embedded in the same concept manifold as legitimate scientific discourse. Detecting semantic validity therefore requires modeling relational structure—claims, constraints, provenance, and ontology—not concept vectors alone.**


