# Code Completion Evaluation Project

## Overview

This project aims to evaluate the effectiveness of a code completion model using a curated dataset from personal repositories. The primary goal was to generate realistic code completion examples and analyze the quality of model-generated completions compared to the actual code. The entire process involved generating a dataset, manually labeling examples, and evaluating the results with various metrics. The project provides a structured approach to assess how well code completion models understand context and generate accurate completions.

## Dataset Generation

The dataset was generated using code from a personal repository, which you can find [here](https://github.com/mvishiu11/CMDChain). Here are the key steps that were taken to prepare the dataset:

1. **Select Code Files ([code](generate/generate_real.py))**: A few files were selected from the repository to provide enough variety for code completion.
2. **Split into Prefix, Middle, and Suffix ([code](generate/generate_real.py))**: Each file was split into three parts: the prefix (code before the cursor), the middle (the part we want the model to predict), and the suffix (code after the cursor). This simulates the real use case where a developer pauses mid-code and waits for the model's suggestion.
3. **Generate Dataset ([code](generate/generate_real.py))**: A Python script was used to automatically split the files and generate examples, resulting in a JSON dataset of 40 examples.
4. **Model Completion ([code](generate/generate_completions.py))**: The dataset was then fed into the [tiny_starcoder_py](https://huggingface.co/bigcode/tiny_starcoder_py) model, which generated code completions for the middle portion based on the prefix and suffix.
5. **Calculate Metrics ([code](utils/calculate_metrics.py))**: Several metrics were computed to assess the quality of each generated completion, including **BLEU score**, **ChrF score**, **exact match**, and **Levenshtein distance**.

## Manual Labeling Process

After generating the code completions, the dataset required manual labeling to understand how well the model performed in each example. To facilitate this process, a [**Streamlit** labeling app](utils/labeling_app.py) was developed:

1. **Streamlit Interface**: A user-friendly interface was built using Streamlit to display each example, including the prefix, suffix, actual middle code, and model-generated completion.
2. **Labeling**: Each example was manually labeled with one of three possible labels:
   - **Correct (1)**: The generated code is correct and matches the intent of the middle code.
   - **Partially Correct (0.5)**: The generated code is mostly correct but requires minor changes.
   - **Incorrect (0)**: The generated code is incorrect or nonsensical.
3. **Progress Tracker**: The labeling app included a GitHub-style progress tracker, which visually showed which examples were labeled and highlighted the current example.
4. **Navigation**: User can navigate between examples using buttons for next, previous, and next/previous unlabeled examples. This made the labeling process efficient.

## Metrics for Evaluation

The following metrics were used to evaluate the model-generated completions:

1. **Exact Match**: Checks if the generated completion exactly matches the actual middle.
2. **BLEU Score**: Measures n-gram overlap between the reference and generated code, providing an understanding of how much of the content was correctly generated.
3. **ChrF Score**: Measures character-level similarity, useful for short segments of code where small differences can be significant.
4. **Levenshtein Distance**: Measures the number of edits needed to convert the generated code to the actual middle, which provides insight into how "far off" the generated completion is.

The metrics were calculated using a [Python script](utils/calculate_metrics.py), which updated the dataset with the metric scores for each example.

## Analysis

The labeled dataset was then used to analyze the performance of the code completion model. The analysis was done using a Jupyter notebook, which included:

1. **Correlation Analysis**: The correlation between manual labels and computed metrics was assessed to determine which metrics aligned best with human judgment.
2. **Visualizations**: Histograms, scatter plots, and other visualizations were used to explore the distribution of metrics, understand model performance, and identify patterns in the generated completions.

## Findings and Learnings

- **BLEU and ChrF Scores**: These metrics provided good insight into the quality of generated completions. Higher correlation with manual labels indicated that these metrics could serve as good proxies for human evaluation.
- **Exact Match and Levenshtein Distance**: While exact match was useful for perfect predictions, it was too strict for partially correct completions. Levenshtein distance helped in quantifying how "close" a completion was, even if it wasn't entirely correct.
- **Manual Labeling Importance**: The labeling process was crucial for understanding nuanced cases where the model produced plausible completions that were technically incorrect.

## How to Run the Project

1. **Dependencies**: Install the required dependencies using `Poetry`.

   ```sh
   poetry install
   ```

2. **Metrics Calculation**: Run the Python script to calculate metrics for the generated completions:

   ```sh
   poetry run python utils/calculate_metrics.py
   ```

3. **Streamlit Labeling App**: To label new datasets or review existing labels, run the Streamlit app:

   ```sh
   poetry run streamlit run utils/labeling_app.py
   ```

4. **Analysis Notebook**: Open the Jupyter notebook for detailed analysis of the dataset and metrics:

   ```sh
   jupyter notebook analysis/eda.ipynb
   ```

## Conclusion

This project provided valuable insights into how well a code completion model like [tiny_starcoder_py](https://huggingface.co/bigcode/tiny_starcoder_py) can understand and generate meaningful completions. The combination of automated metrics and manual labeling enabled a thorough evaluation of model quality, highlighting both strengths and areas for improvement.

Feel free to contribute, fork, or use this project for your own code completion evaluations!