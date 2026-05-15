# Computer Science Research Ethics Pre-Review

## Project Summary

This repository appears to describe a moderation research project using a toxicity detection model for user comments. The README states: “Uses a toxicity detection model for user comments in moderation research” ([README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/README.md:1)). A model card is present and claims to document intended use, limitations, fairness, and deployment boundaries ([docs/model_card.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/docs/model_card.md:1)). The only source file currently contains an import of PyTorch ([src/model.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/src/model.py:1)), with no visible model implementation, training pipeline, dataset handling, evaluation code, or deployment logic.

## Risk Categories And Evidence

### Human Subjects / User Data Risk

The project involves “user comments” ([README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/README.md:1)). That suggests possible handling of human-generated text, which may include personal data, sensitive attributes, harassment, threats, slurs, political views, health information, or other contextual identifiers.

Evidence is limited: the repository does not identify the dataset source, collection process, consent basis, retention policy, anonymization steps, or whether comments are public, private, synthetic, or scraped.

### Moderation And Speech Governance Risk

A toxicity detection model used in moderation research may affect speech classification, content visibility, or downstream moderation decisions. Even if framed as research, this domain has elevated risk because model outputs can encode normative judgments about language, identity terms, dialect, reclaimed slurs, sarcasm, or political speech.

Evidence: the README explicitly names toxicity detection and moderation research ([README.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/README.md:1)). The model card claims deployment boundaries exist, but the repository does not expose the actual boundaries, thresholds, or enforcement workflow ([docs/model_card.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/docs/model_card.md:1)).

### Fairness, Bias, And Disparate Impact Risk

Toxicity models are known to risk higher false-positive rates for identity-related language, minority dialects, quoted abuse, counterspeech, and community-specific language. This repository claims fairness documentation exists, but the visible file only states that a model card documents fairness; it does not provide actual metrics, subgroup analyses, test sets, or mitigation details.

Evidence: fairness is mentioned only as a model-card topic ([docs/model_card.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/docs/model_card.md:1)). No evaluation code or results are present in the inspected files.

### Transparency And Reproducibility Risk

The repository is too sparse to assess the model’s behavior. There is no visible training code, inference code, data schema, dependency file, checkpoint metadata, evaluation script, thresholding policy, or reproducibility instructions. The source file only imports PyTorch ([src/model.py](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/src/model.py:1)).

This limits independent review of whether the model card accurately reflects the implementation.

### Misuse Or Scope Creep Risk

A toxicity classifier developed for “moderation research” could be repurposed for automated enforcement, surveillance of communities, employee/student monitoring, or suppression of controversial speech. The model card reportedly discusses deployment boundaries, but the visible content does not specify prohibited uses or safeguards.

Evidence: intended use and deployment boundaries are mentioned only at a high level ([docs/model_card.md](/Users/tanqinyang/Desktop/cs-ethics-agent/benchmarks/fixtures/case_model_card_present/docs/model_card.md:1)).

## Missing Context And Clarification Questions

- What dataset is used, and how were user comments collected?
- Are comments public, private, scraped, donated, licensed, synthetic, or from a platform partnership?
- Were users informed that their comments could be used for moderation research?
- Does the data include minors, private communities, deleted content, or sensitive topics?
- What labels define “toxicity,” who labeled them, and what disagreement process was used?
- What groups or language varieties were evaluated for fairness?
- What are the false-positive and false-negative rates across identity terms, dialects, languages, and topic areas?
- Is the model intended only for offline research, or could it influence real moderation decisions?
- Are there human review requirements before any enforcement action?
- What deployment boundaries are actually specified in the model card?
- Are raw comments stored in the repository, logs, checkpoints, or external artifacts?
- What privacy-preserving steps are used: redaction, aggregation, minimization, retention limits, access controls?
- Are there mechanisms for appeal, correction, or contestability if outputs affect users?

## Concrete Mitigations

- Add a full data provenance section covering source, license/permission, consent assumptions, collection dates, exclusion criteria, and retention policy.
- Include a clear data minimization plan: avoid storing raw comments unless necessary; redact handles, URLs, names, emails, and other identifiers.
- Document the labeling protocol, annotator instructions, annotator demographics where appropriate, disagreement rates, and examples of edge cases.
- Add subgroup evaluation for identity terms, dialects, reclaimed language, quoted harassment, counterspeech, multilingual content, and political or controversial speech.
- Report calibration, thresholds, precision/recall, false positives, and false negatives across subgroups rather than only aggregate accuracy.
- State explicit non-deployment boundaries, especially prohibiting fully automated punitive moderation without human review.
- Include a harms analysis for over-moderation, under-moderation, chilling effects, and disparate impact.
- Add reproducible evaluation scripts and model implementation details sufficient for reviewers to verify claims.
- Add access controls and retention limits for any real user-comment dataset.
- Add an incident or misuse response plan if the model is shared beyond the research team.

## Advisor Or Review-Body Discussion Questions

- Does the use of user comments require additional review given the source, identifiability, sensitivity, and consent context?
- Is the project purely observational/offline, or could outputs affect real users or platform decisions?
- What level of privacy protection is appropriate for the comment data?
- Are the project’s fairness claims supported by actual subgroup evaluation?
- Who could be harmed by false positives or false negatives, and how severe could those harms be?
- Should the model card be expanded into a more complete release artifact before sharing the model or results?
- What safeguards are needed to prevent research code from becoming an unsupported moderation system?

## Limitations Of This Review

This review is based only on direct inspection of three files: `README.md`, `docs/model_card.md`, and `src/model.py`. The repository contains very little substantive implementation or documentation. I did not use external scanners, repo-ethics MCP tools, or hidden project context. The presence of a model card is useful evidence of intent, but not proof that the project is safe, fair, compliant, or adequately bounded. This is a pre-review, not final ethical approval or rejection.