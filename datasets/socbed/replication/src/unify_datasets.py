import argparse
import json


def main():
    args = parse_args()
    merge({"path": args.file1, "source": args.file1_source},
          {"path": args.file2, "source": args.file2_source})


def parse_args():
    parser = argparse.ArgumentParser(description='Merge and unify two JSONL datasets')
    parser.add_argument("file1", help='Path to first dataset')
    parser.add_argument("file1_source", help="Source of data in file1")
    parser.add_argument("file2", help='Path to second dataset')
    parser.add_argument("file2_source", help="Source of data in file2")
    return parser.parse_args()


def merge(file_1, file_2, path_to_save=None):
    with open(file_1["path"]) as file:
        data_1 = [json.loads(line) for line in file]
    with open(file_2["path"]) as file:
        data_2 = [json.loads(line) for line in file]

    data_1 = normalize_metadata(data_1, file_1["source"])
    data_2 = normalize_metadata(data_2, file_2["source"])

    merged_result = combine_and_sort(data_1, data_2)

    save_result(merged_result, path_to_save)


def normalize_metadata(data, data_source):
    keys_to_keep = ["misuse", "mitreattack", "comment"]
    normalized_data = []

    for alert in data:
        new_metadata = {}
        for key in keys_to_keep:
            if key in alert["metadata"]:
                new_metadata[key] = alert["metadata"][key]
            else:
                # Some fields like "comment" aren't necessarily present
                new_metadata[key] = None
        if "source" in alert["metadata"]:
            # Keep old source if alert already contains one
            new_metadata["source"] = alert["metadata"]["source"]
        else:
            new_metadata["source"] = data_source
        alert["metadata"] = new_metadata
        normalized_data.append(alert)

    return normalized_data


def combine_and_sort(data_1, data_2):
    combined_data = data_1 + data_2
    sorted_data = sorted(combined_data, key=lambda k: k["event"]["@timestamp"])
    return sorted_data


def save_result(data, path):
    file_name = path if path else "merged_dataset.jsonl"
    with open(file_name, "w") as file:
        for entry in data:
            file.write(json.dumps(entry) + "\n")


if __name__ == '__main__':
    main()
