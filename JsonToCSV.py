import json

with open("parsed_disease_ont.json", "r") as f:
	with open("disease_symptoms.txt", "w") as f2:
		for line in f:
			json_text = json.loads(line)
			newLineArr = [json_text["name"]]
			newLineArr += json_text["symptoms"]
			newLine = ",".join(newLineArr) + "\n"
			f2.write(newLine)
