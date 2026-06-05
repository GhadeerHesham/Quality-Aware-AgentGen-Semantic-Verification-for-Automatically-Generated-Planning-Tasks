from dataset_loader import (
    load_dataset,
    get_sample
)

from extractor import (
    extract_environment_text
)

dataset = load_dataset(
    "agentgen_data/merged_gpt_it12.json"
)

sample = get_sample(dataset)

environment_text = extract_environment_text(
    sample
)

print(environment_text[:1000])