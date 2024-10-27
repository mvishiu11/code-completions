import json
import os
import streamlit as st

# Load the dataset
DATA_FILE = os.path.join("data", "dataset.json")


def load_dataset():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_dataset(dataset):
    with open(DATA_FILE, "w") as f:
        json.dump(dataset, f, indent=2)


# Load dataset
dataset = load_dataset()
num_examples = len(dataset)

# Initialize session state variables
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

if "example" not in st.session_state:
    st.session_state.example = dataset[st.session_state.current_index]


# Function to navigate to the next/previous unlabeled example
def move_to_next_unlabeled():
    while st.session_state.current_index < num_examples - 1:
        st.session_state.current_index += 1
        st.session_state.example = dataset[st.session_state.current_index]
        if dataset[st.session_state.current_index].get("label") is None:
            break


def move_to_previous_unlabeled():
    while st.session_state.current_index > 0:
        st.session_state.current_index -= 1
        st.session_state.example = dataset[st.session_state.current_index]
        if dataset[st.session_state.current_index].get("label") is None:
            break


# Navigation buttons
st.sidebar.header("Navigation")
if st.sidebar.button("Previous Example"):
    st.session_state.current_index = max(0, st.session_state.current_index - 1)
    st.session_state.example = dataset[st.session_state.current_index]

if st.sidebar.button("Next Example"):
    st.session_state.current_index = min(
        num_examples - 1, st.session_state.current_index + 1
    )
    st.session_state.example = dataset[st.session_state.current_index]

if st.sidebar.button("Previous Unlabeled Example"):
    move_to_previous_unlabeled()

if st.sidebar.button("Next Unlabeled Example"):
    move_to_next_unlabeled()

st.write(f"**Example {st.session_state.current_index + 1}/{len(dataset)}**")

# Display label status
if (
    "label" in st.session_state.example
    and st.session_state.example["label"] is not None
):
    st.info(f"This example is labeled as: {st.session_state.example['label']}")
else:
    st.warning("This example has not been labeled yet.")

# Code sections
st.subheader("Prefix")
st.code(st.session_state.example["prefix"], language="python")

st.subheader("Suffix")
st.code(st.session_state.example["suffix"], language="python")

st.subheader("Actual Middle")
st.code(st.session_state.example["middle"], language="python")

st.subheader("Model-Generated Completion")
st.code(st.session_state.example["completion"], language="python")

# Display Metrics
st.subheader("Metrics")
if "metrics" in st.session_state.example:
    metrics = st.session_state.example["metrics"]
    st.write(f"- **Exact Match**: {metrics['exact_match']}")
    st.write(f"- **BLEU Score**: {metrics['bleu']:.3f}")
    st.write(f"- **ChrF Score**: {metrics['chrf']:.3f}")
    st.write(f"- **Levenshtein Distance**: {metrics['levenshtein']}")
else:
    st.write("Metrics not available for this example.")

# Labeling options
st.write("### How would you rate the correctness of the model-generated completion?")
label = st.radio(
    "Select a label:",
    options=[1, 0.5, 0],
    index=1,
    format_func=lambda x: {
        1: "Correct (1)",
        0.5: "Partially Correct (0.5)",
        0: "Incorrect (0)",
    }[x],
)

# Save label
if st.button("Save Label"):
    dataset[st.session_state.current_index]["label"] = label
    save_dataset(dataset)
    st.success("Label saved!")

# Progress bar
labeled_count = sum(1 for ex in dataset if ex.get("label") is not None)
st.progress(labeled_count / num_examples)

# Progress tracker
st.sidebar.header("Labeling Progress Tracker")
tracker_cols = 10
tracker_rows = (num_examples + tracker_cols - 1) // tracker_cols

for row in range(tracker_rows):
    cols = st.sidebar.columns(tracker_cols)
    for col_idx in range(tracker_cols):
        example_idx = row * tracker_cols + col_idx
        if example_idx >= num_examples:
            break

        if example_idx == st.session_state.current_index:
            color = "blue"
            border_style = "solid"
        elif dataset[example_idx].get("label") is not None:
            color = "green"
            border_style = "none"
        else:
            color = "red"
            border_style = "none"

        cols[col_idx].markdown(
            f"""
            <div style='width: 20px; height: 20px; background-color: {color};
            border: 2px {border_style} black; margin: auto;'></div>
            <small style='display: block; text-align: center;'>{example_idx + 1}</small>
            """,
            unsafe_allow_html=True,
        )
