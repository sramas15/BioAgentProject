import random

def ReadSymptoms():
	SetOfSymptoms = set([])
	DiseaseToSymptoms = {}
	with open("disease_symptoms.txt", "r") as f:
		for line in f:
			lineArr = line.rstrip().split(",")
			name = lineArr[0]
			symptoms = lineArr[1:]
			DiseaseToSymptoms[name] = symptoms
			SetOfSymptoms = SetOfSymptoms.union(set(symptoms))
	return (SetOfSymptoms, DiseaseToSymptoms)

(SET_OF_SYMPTOMS, DISEASE_TO_SYMPTOMS) = ReadSymptoms()

def GetPatient(disease, prob_has_symptom=0.8, prob_has_rand_symptom=0.0):
	if disease not in DISEASE_TO_SYMPTOMS:
		raise ValueError("Disease not found")
	symptoms = []
	for symptom in DISEASE_TO_SYMPTOMS[disease]:
		if random.random() < prob_has_symptom:
			symptoms.append(symptom)
	for symptom in SET_OF_SYMPTOMS:
		if random.random() < prob_has_rand_symptom:
			symptoms.append(symptom)
	return set(symptoms)


if __name__ == "__main__" : GetPatient("inhalation anthrax")