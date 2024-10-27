from transformers import AutoTokenizer, AutoModelForCausalLM
import json
import os
import torch

model_name = "bigcode/tiny_starcoder_py"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)


def complete_code(prefix, suffix):
    prompt = prefix + "\n"
    inputs = tokenizer(prompt, return_tensors="pt")

    model.eval()

    with torch.no_grad():
        output_ids = model.generate(
            **inputs, max_length=len(inputs["input_ids"][0]) + 50
        )

    completion = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    return completion[len(prefix) :]


completions = []
dataset_path = os.path.join("data", "real.json")
output_path = os.path.join("data", "completions.json")

with open(dataset_path, "r") as file:
    dataset = json.load(file)

for example in dataset:
    prefix = example["prefix"]
    suffix = example["suffix"]
    try:
        completion = complete_code(prefix, suffix)
        completions.append(
            {
                "prefix": prefix,
                "middle": example["middle"],
                "suffix": suffix,
                "completion": completion,
            }
        )
    except Exception as e:
        print(f"Error while processing example: {example} \n Error: {e}")
        continue

with open(output_path, "w") as outfile:
    json.dump(completions, outfile, indent=2)
