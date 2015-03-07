from baseClass import *

transmissionFile = '../testDataBasic/transmission_methods.txt'
findingFile = '../testDataBasic/findings.txt' 
pMethodFile = '../testDataBasic/pMethods.txt' 
agentFile= '../testDataBasic/agents.txt'
agentFullFile = '../data/agents.txt'
pMethodFullFile = '../data/pMethods.tsv'

"""Basic sanity check for initializing an ontology,
using test data found in folder testDataBasic"""
#o = Ontology('test ontology')
#o.initialize(transmissionFile, findingFile, pMethodFile, agentFile)

"""Basic sanity check for initializing an ontology,
using full agent data found in folder data"""
print "============== Test Ontology =============="
o = Ontology('test full ontology')
o.initialize(transmissionFile, findingFile, pMethodFullFile, agentFullFile)
print o

"""Basic test for diagnosis, using Machupo hemorrhagic fever"""
print "============== Test Diagnosis =============="
p = Patient(o, 0, "X", 1)
o.addPatient(p)
#symptoms = ["fever","chills","cough","difficulty breathing"]
symptoms = ["fever","headache","fatigue","myalgia","arthralgia", \
	"bleeding from the oral and nasal mucosa","bleeding from the bronchopulmonary", \
	"hemorrhage from nasal and oral","tremors","seizure"]
for symptom in symptoms:
	p.addFinding(symptom)
p.determineDiagnosis()
s = 0.0
for diagnosis in  p.pDiagnosis:
	s += diagnosis.score
	print diagnosis

print "============== Test Prevention =============="
methodToScore = p.determinePreventionMethods(400.0)
max_score = max(methodToScore.values())
print "===== scores ======"
for method in methodToScore:
	print method, (methodToScore[method])
print "===== returned methods ======"
for method in p.pMethods:
	print method

print "============== Test Diagnosis =============="
p = Patient(o, 0, "Y", 2)
o.addPatient(p)
for symptom in symptoms:
	p.addFinding(symptom)
p.determineDiagnosis()
s = 0.0
for diagnosis in  p.pDiagnosis:
	s += diagnosis.score
	print diagnosis

print "============== Test Prevention =============="
methodToScore = p.determinePreventionMethods(300.0)
max_score = max(methodToScore.values())
print "===== scores ======"
for method in methodToScore:
	print method, (methodToScore[method])
print "===== returned methods ======"
for method in p.pMethods:
	print method