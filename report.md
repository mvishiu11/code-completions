# Code Completion Evaluation Project Report

## Introduction

The Code Completion Evaluation Project aimed to assess the quality and accuracy of a code completion model, specifically [tiny_starcoder_py](https://huggingface.co/bigcode/tiny_starcoder_py), using a dataset curated from a personal repository. This project involved generating code completion examples, labeling the generated code, evaluating the results with various metrics, and conducting an in-depth exploratory data analysis (EDA). This report documents the entire process, including our findings, learnings, and future recommendations.

## Dataset Generation

The dataset used in this project was generated using selected files from the repository [CMDChain](https://github.com/mvishiu11/CMDChain). The process involved:

1. **Code Selection and Segmentation**: A set of code files was selected to ensure variety in the examples. Each file was then split into three parts:
   - **Prefix**: Code before the cursor position.
   - **Middle**: Code that is missing and needs to be predicted.
   - **Suffix**: Code after the cursor position.

   This segmentation simulates a real-world scenario where a developer pauses mid-code and expects the completion model to suggest the next line or function.

2. **Dataset Preparation**: A script (`generate_real.py`) was used to generate 40 examples consisting of prefix, middle, and suffix segments.

3. **Model Completion**: The dataset was then passed through the `tiny_starcoder_py` model to generate code completions for each example's middle segment. This resulted in a dataset with 40 model-generated completions.

4. **Metric Calculation**: To evaluate the generated completions, we calculated the following metrics using a script (`calculate_metrics.py`):
   - **BLEU Score**
   - **ChrF Score**
   - **Exact Match**
   - **Levenshtein Distance**

These metrics were added to each example to facilitate further analysis.

## Manual Labeling Process

To gain a deeper understanding of the model’s performance, a manual labeling process was undertaken:

1. **Streamlit App**: A labeling interface was developed using Streamlit (`labeling_app.py`) to display each example with the prefix, suffix, actual middle, and model-generated completion.

2. **Labeling Criteria**: Each example was manually labeled as:
   - **Correct (1)**: Generated code matches the intent of the actual middle.
   - **Partially Correct (0.5)**: Code is mostly correct but requires some changes.
   - **Incorrect (0)**: Code is incorrect or nonsensical.

3. **Progress Tracker**: The app included a progress tracker and navigation buttons, making it easier to move between examples and understand the progress of the labeling process.

## Metrics for Evaluation

The metrics used for evaluating the model-generated completions were:

1. **Exact Match**: Checks if the generated completion exactly matches the actual middle code. This metric was ultimately dropped due to the lack of exact matches in the dataset.
2. **BLEU Score**: Measures n-gram overlap, providing insight into how closely the generated content matches the reference.
3. **ChrF Score**: Character-level similarity, useful for evaluating code where small differences can be important.
4. **Levenshtein Distance**: Measures the number of edits needed to transform the generated code to the reference, indicating how "far off" the generated code is.

## Exploratory Data Analysis (EDA)

The labeled dataset, along with the computed metrics, was analyzed using a Jupyter notebook. Here are the key findings from the EDA:

### Label Distribution
- The dataset was **imbalanced**, with **55% of examples labeled as incorrect**, **25% as partially correct**, and **20% as correct**.
- The imbalance may have impacted metric correlation analysis, as there were fewer correct completions.

### Metrics Overview
- **Exact Match** had zero matches and was deemed useless for this analysis.
- **BLEU and ChrF Scores** both showed limited correlation with manual labels, indicating they might not be effective in evaluating code quality.
- **Levenshtein Distance** showed a wide distribution, reflecting large variability in code similarity.

### Correlation Analysis
- The correlation between **BLEU Score** and manual labels was **0.17**, indicating a **weak positive correlation**.
- **ChrF Score** and **Levenshtein Distance** both had near-zero or negative correlations (`-0.039` and `-0.14`, respectively), suggesting these metrics were also insufficient for evaluating code quality.
- **BLEU and ChrF Scores** were highly correlated with each other (`0.69`), indicating redundancy.

### Outlier Analysis
- **BLEU** and **ChrF** metrics had several **outliers** with high scores, but the majority of values were clustered near zero. This suggests the model often failed to generate meaningful completions, but occasionally produced more accurate ones.
- **Levenshtein Distance** showed significant variability, with some completions being close to the reference and others far off, suggesting inconsistent model performance.

## Key Findings and Learnings

- **Metric Limitations**: The standard metrics (BLEU, ChrF, Levenshtein) were not effective at capturing the quality of the code completions in this dataset. The lack of correlation with manual labels highlighted the importance of using more **code-specific metrics**, such as **CodeBLEU**.
- **Manual Labeling and Dataset Imbalance**: The imbalance in the dataset led to limited opportunities for metrics to learn from correct completions. More balanced examples would improve analysis reliability.
- **Redundancy in Metrics**: **BLEU** and **ChrF** showed high correlation, suggesting that using both is unnecessary for future analysis.
- **Qualitative Analysis Needed**: Some examples with high BLEU or ChrF scores but incorrect labels indicate that these metrics do not fully capture code quality. Qualitative examination of such examples is crucial to understand where metrics fall short.

## Recommendations

1. **Adopt Code-Specific Metrics**: Implement metrics like **CodeBLEU** for future analysis to better capture the quality of code completions, considering syntax and semantics.
2. **Improve Dataset Balance**: Balance the dataset with more examples of correct and partially correct completions to avoid skewed correlations.
3. **Refine Metric Selection**: Drop redundant metrics like **ChrF** if **BLEU** is being used, or vice versa, to simplify evaluation.
4. **Include Qualitative Evaluation**: Qualitative analysis of high-scoring completions with low manual labels will provide more insight into the strengths and weaknesses of the model.

## Conclusion

This project provided valuable insights into the evaluation of code completion models. Automated metrics like BLEU and ChrF, which are well-known in NLP, showed limitations in evaluating code quality accurately. A combination of manual labeling and EDA helped to identify these limitations, emphasizing the need for **code-specific metrics** and **balanced datasets** for more effective analysis. By incorporating these learnings, future evaluations can better understand how well code completion models align with developer expectations.