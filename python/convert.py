import json
import csv
import os

metadata_csv = "./metadata.csv"
# valuable_attr = "face"
try:
    os.remove(metadata_csv)
except:
    print("Can't remove" + metadata_csv)


def json_to_csv(json_data):
    # Extracting required fields from JSON data
    name = json_data["name"]
    description = json_data["description"]
    file_name = json_data["image"].split("/")[-1]
    # external_url = f"https://example.com/{token_id}"
    external_url = " "

    attributes_dict = {}
    # valuable_attr_value = ""
    for attribute in json_data["attributes"]:
        attributes_dict["attributes[" + attribute["trait_type"].title() + "]"] = attribute["value"]
        # if attribute["trait_type"].upper() == valuable_attr.upper():
        #     valuable_attr_value = attribute["value"]
    # Writing to CSV
    with open(metadata_csv, "a", newline="") as csvfile:
        fieldnames = ["tokenID", "name", "description", "file_name", "external_url"] + list(attributes_dict.keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the file is empty, write the header
        if os.path.getsize(metadata_csv) == 0:
            writer.writeheader()

        writer.writerow(
            {
                "tokenID": name.split("#")[-1],
                "name": name,
                "description": description,
                "file_name": file_name,
                "external_url": external_url,
                **attributes_dict,
            }
        )


def convert_json_files_to_csv(directory):
    # Function to extract the numerical part of the filename
    def numerical_part(filename):
        return int("".join(filter(str.isdigit, filename)))

    # Get a sorted list of filenames based on their numerical part
    filenames = sorted(os.listdir(directory), key=numerical_part)

    # Iterate over each JSON file in the sorted list
    for filename in filenames:
        if filename.endswith(".json"):
            with open(os.path.join(directory, filename)) as json_file:
                json_data = json.load(json_file)
                json_to_csv(json_data)


# Convert JSON files to CSV and append to output CSV file
json_directory = "../build/json"
convert_json_files_to_csv(json_directory)
