DEFINITIVE_FACTOR = 2
INPUT_FILE = "data/AgentsDB.tsv"
OUTPUT_FILE = "data/agents.txt"
FORMAT_LINE = "Disease	Finding	Transmission Method (Comma separated list)	Reproductive Number	Incubation Period (days)	Mortality Rate UnTreated	Mortality Rate Treated	Gram Stain	Infectious Dose\n"

# Compute Trigger rates (not weighted)
symptom_freq = {}
with open("disease_symptoms.txt", "r") as f:
	for line in f:
		arr = line.split(",")
		for i in range(len(arr)):
			symptom = arr[i].strip()
			if symptom not in symptom_freq:
				symptom_freq[symptom] = 0
			symptom_freq[symptom] += 1
triggering_rate = {}
for symptom in symptom_freq:
	triggering_rate[symptom] = 1.0/symptom_freq[symptom]


# Read input file
with open(INPUT_FILE, "r") as f:
	with open(OUTPUT_FILE, "w") as o:
		# write the title line
		o.write(FORMAT_LINE)
		isFirstLine = True
		for line in f:
			# Skip title line
			if isFirstLine:
				isFirstLine = False
				continue


			[disease, findings, defFindings, transmission, rNum, iNum, mNumU, mNumT, stain, dose] = line.split("\t")

			# Find the associated trigger rate for each finding
			findingWeights = {}
			for finding in findings.split(","):
				finding = finding.strip()
				findingWeights[finding] = triggering_rate[finding]

			# Scale the triggering rate for definitive factors
			for finding in defFindings.split(","):
				finding = finding.strip()
				findingWeights[finding] *= DEFINITIVE_FACTOR

			# Create output string for triggering findings
			findingStr = ""
			for finding in findingWeights:
				findingStr += "%s=%f," % (finding, findingWeights[finding])
			findingStr = findingStr.rstrip(",")

			# Write out the formatted agent string
			o.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (disease, findingStr, transmission, rNum, iNum, mNumU, mNumT, stain, dose))

