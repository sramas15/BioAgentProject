import requests
import json

URL_IDs = ["0050160", "7426", "0050059", "0050352", "10398", "0050508", "14239", "2122", "0050383", "4325", "4327", "9537", "0050195"]
OUTPUT_FILE = "parsed_disease_ont.json"
URL_PREFIX = "http://www.disease-ontology.org/api/metadata/DOID:%s"

with open(OUTPUT_FILE, "w") as f:
	for doid in URL_IDs:
		url = URL_PREFIX % doid
		r = requests.get(url)
		json_text = json.loads(r.text)
		defn = json_text['definition']
		symptoms = []
		i = 0
		for string in defn.split("has_symptom"):
			if i != 0:
				symptoms.append(string.split(",")[0].split(".")[0].strip(", ."))
			i += 1
		i = 0
		for string in defn.split("results_in_formation_of"):
			if i != 0:
				symptoms.append(string.split(",")[0].split(".")[0].strip(", ."))
			i += 1
		i = 0
		for string in defn.split("results_in"):
			if i != 0:
				symptoms.append(string.split(",")[0].split(".")[0].strip(", ."))
			i += 1
		json_text["symptoms"] = symptoms
		json.dump(json_text, f)
		f.write("\n")
