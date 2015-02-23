import requests
import json

URL_IDs = ["9159", "7426"]
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
				symptoms.append(string.split("and")[0].split(".")[0].strip(", ."))
			i += 1
		json_text["symptoms"] = symptoms
		json.dump(json_text, f)
		f.write("\n")
