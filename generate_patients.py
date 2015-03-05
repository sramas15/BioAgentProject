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
DATE = "date"
END_OF_DAY_DELIM = -1

def CreatePotentialPatients(numPotentialPatients):
    Patients = []
    # Initialize patients list
    for i in range(numPotentialPatients):
        Patients.append({})
    return Patients

def CreateContactsBetweenPotentialPatients(Patients, probOfContact):
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

def InfectWithDisease(Patients, disease, probInfect, probCarrier, decayFactor, initialDate):
	 # Create initial patient with disease
    patient_x = 0
    symptom_prob = 0.9
    date = initialDate
    Patients[patient_x][SYMPTOMS] = GetPatient(disease, symptom_prob, probRandomSymptom)
    Patients[patient_x][DATE] = date
    date += 1

    # Infect neighbors
    q = Queue.Queue()
    for neighbor in Patients[patient_x][CONTACTS]:
        q.put(neighbor)
    q.put(END_OF_DAY_DELIM)
    infected = set([patient_x])
    consec_delim = 0
    while not q.empty():
    	# Increment date when reach the end of each of each level in the BFS
    	if consec_delim > 1:
        	break
        curr_patient = q.get()
        if curr_patient == END_OF_DAY_DELIM:
        	date += 1
        	symptom_prob *= decayFactor # simulate passage of time; later a patient infected, less likely to show all symptoms
        	consec_delim += 1
        	continue
        else:
        	consec_delim = 0

        # With probablity probInfect, infect this neighbor
        if random.random() < probInfect:
            infected.add(curr_patient)
            Patients[curr_patient][SYMPTOMS] = GetPatient(disease, symptom_prob, probRandomSymptom)
            Patients[curr_patient][DATE] = date
            for neighbor in Patients[curr_patient][CONTACTS]:
                if neighbor not in infected: # Already infected, no point infecting again...
                    q.put(neighbor)
        # With probability probCarrier, could be a carrier for disease (but not actually infeced)
        # probability infect neighbor is probCarrier*probInfect
        elif random.random() < probCarrier:
            for neighbor in Patients[curr_patient][CONTACTS]:
                if neighbor not in infected:
                    q.put(neighbor)

def AddRandomSymptomsToUninfected(Patients, probRandomSymptom, dateStart, dateEnd):
    for i in range(numPatients):
        if SYMPTOMS not in Patients[i]:
            Patients[i][SYMPTOMS] = GetPatient(disease, 0.0, probRandomSymptom)
            if len(Patients[i][SYMPTOMS]) > 0:
            	Patients[i][DATE] = random.randint(dateStart, dateEnd)





if __name__ == "__main__" : print "x"

