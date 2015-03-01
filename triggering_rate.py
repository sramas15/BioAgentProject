symptom_freq = {}
with open("disease_symptoms.txt", "r") as f:
	for line in f:
		arr = line.split(",")
		for i in range(1, len(arr)):
			symptom = arr[i].rstrip()
			if symptom not in symptom_freq:
				symptom_freq[symptom] = 0
			symptom_freq[symptom] += 1
triggering_rate = {}
for symptom in symptom_freq:
	triggering_rate[symptom] = 1.0/symptom_freq[symptom]
	print "%s : %f" % (symptom, triggering_rate[symptom])
