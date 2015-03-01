import random
import Queue

COMMON_SYMPTOMS = set(['hiccups', 'diarrhea','joint pain','tiredness', 'mild fever', 'blurred vision','difficulty breathing','rash','red eyes', 'bleeding', 'headache', 'muscle aches', 'loss of appetite', 'fever', 'chills', 'weakness', 'infection', 'vomiting', 'fatigue', 'stomach pain', 'cough', 'weight loss', 'sore throat', 'nausea', 'chest pain', 'shortness of breath', 'chest discomfort'])

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

def GetPatient(disease, prob_has_symptom=0.8, prob_has_rand_symptom=0.01):
	if disease not in DISEASE_TO_SYMPTOMS:
		raise ValueError("Disease not found")
	symptoms = []
	for symptom in DISEASE_TO_SYMPTOMS[disease]:
		if random.random() < prob_has_symptom:
			symptoms.append(symptom)
	for symptom in COMMON_SYMPTOMS:
		if random.random() < prob_has_rand_symptom:
			symptoms.append(symptom)
	return set(symptoms)

CONTACTS = "contact"
SYMPTOMS = "symptoms"

def GenPatients(disease, probOfContact, probInfect, probCarrier, numPatients, decayFactor, probRandomSymptom):
	Patients = []
	# Initialize patients list
	for i in range(numPatients):
		Patients.append({})

	# Determine who each patient was in contact with
	for i in range(numPatients):
		for j in range(i+1, numPatients):
			if random.random() < probOfContact:
				if CONTACTS not in Patients[i]:
					Patients[i][CONTACTS] = []
				Patients[i][CONTACTS].append(j)
				if CONTACTS not in Patients[j]:
					Patients[j][CONTACTS] = []
				Patients[j][CONTACTS].append(i)

	# Create initial patient with disease
	patient_x = 0
	symptom_prob = 0.9
	Patients[patient_x][SYMPTOMS] = GetPatient(disease, symptom_prob, probRandomSymptom)

	# Infect neighbors
	q = Queue.Queue()
	for neighbor in Patients[patient_x][CONTACTS]:
		q.put(neighbor)
	infected = set([patient_x])
	while not q.empty():
		curr_patient = q.get()
		# With probablity probInfect, infect this neighbor
		if random.random() < probInfect:
			infected.add(curr_patient)
			Patients[curr_patient][SYMPTOMS] = GetPatient(disease, symptom_prob, probRandomSymptom)
			for neighbor in Patients[curr_patient][CONTACTS]:
				if neighbor not in infected: # Already infected, no point infecting again...
					q.put(neighbor)
			symptom_prob *= decayFactor # simulate passage of time; later a patient infected, less likely to show all symptoms
		# With probability probCarrier, could be a carrier for disease (but not actually infeced)
		# probability infect neighbor is probCarrier*probInfect
		elif random.random() < probCarrier:
			for neighbor in Patients[curr_patient][CONTACTS]:
				if neighbor not in infected:
					q.put(neighbor)
			symptom_prob *= decayFactor # simulate passage of time; later a patient infected, less likely to show all symptoms

	# Given remaining patients random symptoms
	for i in range(numPatients):
		if SYMPTOMS not in Patients[i]:
			Patients[i][SYMPTOMS] = GetPatient(disease, 0.0, probRandomSymptom)

	return Patients






if __name__ == "__main__" : print GenPatients('inhalation anthrax', 0.05, 0.5, 0.2, 20, 0.9, 0.01)

