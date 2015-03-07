from baseClass import *

transmissionFile = '../testDataBasic/transmission_methods.txt'
findingFile = '../testDataBasic/findings.txt' 
pMethodFile = '../testDataBasic/pMethods.txt' 
agentFile= '../testDataBasic/agents.txt'
agentFullFile = '../data/agents.txt'

"""Basic sanity check for initializing an ontology,
using test data found in folder testDataBasic"""
#o = Ontology('test ontology')
#o.initialize(transmissionFile, findingFile, pMethodFile, agentFile)

"""Basic sanity check for initializing an ontology,
using full agent data found in folder data"""
o = Ontology('test full ontology')
o.initialize(transmissionFile, findingFile, pMethodFile, agentFullFile)
print o

"""Basic test for diagnosis, using Machupo hemorrhagic fever"""
p = Patient(o, 0, "X", 1)
o.addPatient(p)
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

p.determinePreventionMethods(0.0)

for pMethod in p.pMethods:
	print pMethod