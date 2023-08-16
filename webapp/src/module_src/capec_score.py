import os
import shutil
import json
import csv
import urllib.request
import zipfile
import re

from statistics import mean


def main():
    pass


def process(
        dataset,
        mult_score_handling,
        severity_weight=1,
        likelihood_weight=1
):
    capec_scores_json = load_capec_scores()
    events = dataset["data"]

    for index, sre in enumerate(events):
        capec_score = None

        if "tags" in sre["rule"]:
            techniques = sre["rule"]["tags"]
            capec_score = get_capec_score(
                capec_scores_json, severity_weight, likelihood_weight, techniques, mult_score_handling)

        if capec_score is None:
            continue  # keep old score
        else:
            sre.setdefault("event", {})
            sre["event"].setdefault("event", {})
            sre["event"]["event"]["risk_score"] = capec_score
            sre["event"]["event"]["base_score"] = capec_score
            events[index] = sre

    dataset["data"] = events
    return dataset


def get_capec_score(capec_scores, s_weight, l_weight, techniques, mult_score_handling):
    # to match technique IDs like t1234.123 or t1234
    id_pattern = r"t\d{4}(\.\d{3})?"
    id_pattern_subtechnique = r"t\d{4}\.\d{3}"

    scores = []

    for technique in techniques:
        technique = technique.replace("attack.", "")

        # if it is a valid technique, and we have some CAPEC score for that technique, calculate the total score
        if re.match(id_pattern, technique) and technique in capec_scores:
            new_score = calculate_combined_score(
                capec_scores[technique]["severity_score"],
                capec_scores[technique]["likelihood_score"],
                s_weight,
                l_weight
            )
            scores.append(new_score)
        # if it is a sub-technique and cannot be found, look for parent technique
        elif re.match(id_pattern_subtechnique, technique) and technique[:5] in capec_scores:
            parent_technique = technique[:5]
            new_score = calculate_combined_score(
                capec_scores[parent_technique]["severity_score"],
                capec_scores[parent_technique]["likelihood_score"],
                s_weight,
                l_weight
            )
            scores.append(new_score)
        else:
            pass

    if not scores:
        return None
    elif mult_score_handling == "highest":
        return max(scores)
    elif mult_score_handling == "mean":
        return int(mean(scores))


def calculate_combined_score(s_score, l_score, s_weight, l_weight):
    max_score = s_weight * 5 + l_weight * 5

    severity_score = s_score if s_score else 0
    likelihood_score = l_score if l_score else 0
    new_score = severity_score * s_weight + likelihood_score * l_weight

    norm_score = (new_score / max_score) * 100
    return norm_score


############################################################################
# Everything past here is just for the generation of the capec_scores.json #
############################################################################

def load_capec_scores():
    this_path = os.path.abspath(__file__)
    data_path = os.path.join(os.path.dirname(this_path), "resources/capec_scores.json")

    if not os.path.exists(data_path):
        create_capec_json(data_path)

    with open(data_path, "r") as file:
        return json.load(file)


def create_capec_json(path):
    csv_reader = obtain_csv_data()
    headers = next(csv_reader)
    likelihood = headers.index('Likelihood Of Attack')
    severity = headers.index('Typical Severity')
    mappings = headers.index('Taxonomy Mappings')

    capec_score_dict = {}
    for entry in csv_reader:
        techniques = get_techniques(entry[mappings])
        new_likelihood = get_numerical_score(entry[likelihood].lower())
        new_severity = get_numerical_score(entry[severity].lower())

        for technique in techniques:
            # Scores can differ! For example "t1574.010" with IDs 1, 17 and 180
            # For now, we just take the higher value
            old_severity = capec_score_dict.get(technique, {}).get("severity_score")
            old_likelihood = capec_score_dict.get(technique, {}).get("likelihood_score")

            severity_score = calculate_score(new_severity, old_severity)
            likelihood_score = calculate_score(new_likelihood, old_likelihood)

            if severity_score is None and likelihood_score is None:
                pass
            else:
                capec_score_dict[technique] = {
                    "likelihood_score": likelihood_score,
                    "severity_score": severity_score,
                }

    capec_score_dict = dict(sorted(capec_score_dict.items()))
    with open(path, "w") as file:
        json.dump(capec_score_dict, file, indent=4)


def calculate_score(old_score, new_score):
    if old_score is None:
        return new_score
    elif new_score is None:
        return old_score
    elif old_score >= new_score:
        return old_score
    else:
        return new_score


def obtain_csv_data():
    url = "https://capec.mitre.org/data/csv/658.csv.zip"
    zipped_csv = urllib.request.urlopen(url).read()

    tmp_dir = handle_tmp_dir()
    temp_file = os.path.join(tmp_dir, "temp.zip")
    with open(temp_file, "wb") as file:
        file.write(zipped_csv)

    with zipfile.ZipFile(temp_file, "r") as zip_ref:
        csv_file = os.path.join(tmp_dir, zip_ref.namelist()[0])
        zip_ref.extract(zip_ref.namelist()[0], path=tmp_dir)

    with open(csv_file, "r") as file:
        csv_data = file.read()

    handle_tmp_dir(dir_to_delete=tmp_dir)
    return csv.reader(csv_data.splitlines())


def handle_tmp_dir(dir_to_delete=None):
    if not dir_to_delete:
        current_directory = os.getcwd()
        tmp_directory = os.path.join(current_directory, "tmp")
        # Don't supress error if dir already exists, just in case there might be something important
        os.makedirs(tmp_directory)
        return tmp_directory
    else:
        shutil.rmtree(dir_to_delete)


def get_techniques(mappings):
    # "Taxonomy Mappings" entry looks like this
    # TAXONOMY NAME:ATTACK:ENTRY ID:1110:ENTRY NAME:Brute Force::::
    # TAXONOMY NAME:WASC:ENTRY ID:11:ENTRY NAME:Brute Force::::
    # TAXONOMY NAME:OWASP Attacks:ENTRY NAME:Brute force attack::
    # aka split by :::: and then by :
    techniques = []
    entries = mappings.split("::::")
    for entry in entries:
        data = entry.split(":")
        if data[1] == "ATTACK":
            techniques.append(f"t{data[3]}")
    return techniques


def get_numerical_score(string_score):
    if not string_score:
        # Some entries don't have a certain score
        return None
    elif string_score == "very low" or string_score == "informational":
        return 1
    elif string_score == "low":
        return 2
    elif string_score == "medium":
        return 3
    elif string_score == "high":
        return 4
    elif string_score == "very high" or string_score == "critical":
        return 5
    else:
        raise ValueError("Unexpected score string")


if __name__ == '__main__':
    main()
