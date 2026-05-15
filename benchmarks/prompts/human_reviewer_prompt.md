# Human Reviewer Labeling Prompt

Review the synthetic fixture and its gold label.

Check:

- expected risk categories
- expected missing-context categories
- expected positive controls
- expected absent categories
- required evidence paths
- forbidden or overclaiming language expectations

Mark `review_status` as `reviewed` only after confirming that the label reflects the fixture content and is not copied from scanner output.
