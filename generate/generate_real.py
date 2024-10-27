import os
import random
import json


def split_code(file_path, num_examples):
    with open(file_path, "r") as f:
        code_lines = f.readlines()

    if len(code_lines) < 10:
        return []

    examples = []
    for _ in range(num_examples):
        split_index = random.randint(5, len(code_lines) - 5)
        prefix = "".join(code_lines[:split_index])
        suffix = "".join(code_lines[split_index + 1 :])
        middle = code_lines[split_index]

        examples.append({"prefix": prefix, "middle": middle, "suffix": suffix})

    return examples


def generate_dataset(directory, num_examples_per_file=10):
    dataset = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                examples = split_code(file_path, num_examples_per_file)
                dataset.extend(examples)

    return dataset


# Usage
dataset = generate_dataset("./cmd_chain", num_examples_per_file=10)
json.dump(dataset, open(os.path.join("data", "real.json"), "w"), indent=2)
print(f"Generated {len(dataset)} examples.")
