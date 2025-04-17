import json


def remove_duplicates(input_file, output_file):
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    unique_entries = []
    seen_entries = set()

    for entry in data:
        # Create a tuple of all label fields to identify duplicates
        entry_id = (
            entry.get("label_uk", ""),
            entry.get("label_ru", ""),
            entry.get("label_gr", ""),
            entry.get("label_en", ""),
        )
        if entry_id not in seen_entries:
            seen_entries.add(entry_id)
            unique_entries.append(entry)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(unique_entries, f, ensure_ascii=False, indent=2)

    print(
        f"Removed duplicates. Original entries: {len(data)}, Unique entries: {len(unique_entries)}"
    )


if __name__ == "__main__":
    input_file = "codex.json"  # Replace with your input file name
    output_file = "codex_cleaned.json"  # Replace with your desired output file name
    remove_duplicates(input_file, output_file)
