import math
import random
from baseClass import *

transmissionFile = '../testDataBasic/transmission_methods.txt'
findingFile = '../testDataBasic/findings.txt' 
pMethodFile = '../testDataBasic/pMethods.txt' 
agentFile= '../testDataBasic/agents.txt'
agentFullFile = '../data/agents.txt'
pMethodFullFile = '../data/pMethods.tsv'

def createPatients(ontology, disease, prob_finding, decay, num_days, other_disease, prob_other):
    patients = []
    actual_diagnosis = []
    agent = ontology.getAgentByName(disease)
    assert agent != None
    other_agent = ontology.getAgentByName(other_disease)
    assert other_agent != None
    num_days = float(num_days)
    cycles = int(min(math.ceil(num_days/agent.incubationPeriod), 7.0))
    num_patients = sum(math.ceil(pow(agent.rNumber, a)) for a in range(0, cycles+1))
    ID = 0
    lastIdInLevel = -1
    date = 0
    for a in range(0, cycles+1):
        for b in range(0, int(math.ceil(pow(agent.rNumber, a)))):
            p = Patient(ontology, ID, str(ID), date)
            ontology.addPatient(p)
            agentUsed = agent
            if random.random() < prob_other:
                agentUsed = other_agent
            actual_diagnosis.append(agentUsed)
            index = random.randint(0, len(agentUsed.tFindings)-1)
            p.addFinding(list(agentUsed.tFindings)[index].finding.definition)
            for tFinding in agentUsed.tFindings:
                if random.random() < prob_finding:
                    p.addFinding(tFinding.finding.definition)
            if lastIdInLevel != -1:
                p.addContacts(set([lastIdInLevel]))
            ID += 1
            patients.append(p)
        lastIdInLevel = ID - 1
        date += 1
        prob_finding *= decay
    return (patients, actual_diagnosis)

def runEvaluationDiagnosis(ontology, disease, prob_finding, decay, num_days, other_disease, prob_other):
    (patients, actual_diagnosis) = createPatients(ontology, disease, prob_finding, decay, num_days, other_disease, prob_other)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(0, len(patients)):
        p = patients[i]
        p.determineDiagnosis()
        max_prob = 0.0
        agent = None
        for diagnosis in p.pDiagnosis:
            if diagnosis.score > max_prob:
                max_prob = diagnosis.score
                agent = diagnosis.agent
        if agent.name == disease and agent == actual_diagnosis[i]:
            tp += 1
        if agent.name == disease and agent != actual_diagnosis[i]:
            fp += 1
        if agent.name != disease and agent == actual_diagnosis[i]:
            tn += 1
        if agent.name != disease and agent != actual_diagnosis[i]:
            fn += 1
    print "Sensitivity: %f" % (float(tp)/(tp+fn))
    print "Specificity: %f" % (float(tn)/(fp+tn))

if __name__ == "__main__":
    o = Ontology('test full ontology')
    o.initialize(transmissionFile, findingFile, pMethodFullFile, agentFullFile)
    runEvaluationDiagnosis(o, "Pneumonic plague", 0.8, 0.9, 365, "Bubonic plague", 0.2)
