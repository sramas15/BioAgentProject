with open('disease_symptoms.txt') as f:
	with open('finding_list.txt', 'w') as outF:
		findings = set()
		for line in f:
			data = line.rstrip().split(',')
			for symptom in data[1:]:
				findings.add(symptom)

		for finding in findings:
			outF.write(finding)
			outF.write('\n')