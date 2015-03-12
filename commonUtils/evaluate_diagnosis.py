import math
import random
from baseClass import *

transmissionFile = '../testDataBasic/transmission_methods.txt'
findingFile = '../testDataBasic/findings.txt' 
pMethodFile = '../testDataBasic/pMethods.txt' 
agentFile= '../testDataBasic/agents.txt'
agentFullFile = '../data/agents.txt'
pMethodFullFile = '../data/pMethods.tsv'

def createPatients(ontology, disease, prob_finding, decay, num_days, other_disease, prob_other, cycles=-1):
    ontology.clearPatients()
    patients = []
    actual_diagnosis = []
    agent = ontology.getAgentByName(disease)
    assert agent != None
    other_agent = ontology.getAgentByName(other_disease)
    assert other_agent != None
    num_days = float(num_days)
    if cycles == -1:
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
            num_findings = 0
            for tFinding in agentUsed.tFindings:
                if random.random() < prob_finding:
                    num_findings += 1
                    p.addFinding(tFinding.finding.definition)
            if num_findings == 0:
                p.addFinding(list(agentUsed.tFindings)[index].finding.definition)
            if lastIdInLevel != -1:
                p.addContacts(set([lastIdInLevel]))
            ID += 1
            patients.append(p)
        lastIdInLevel = ID - 1
        date += 1
        prob_finding *= decay
    return (patients, actual_diagnosis)


def runEvaluationPrevention(ontology, disease, prob_finding, decay, num_days, other_disease, prob_other, preventionMethod):
    (patients, actual_diagnosis) = createPatients(ontology, disease, prob_finding, decay, num_days, other_disease, prob_other, 7)
    for i in range(0, len(patients)):
        p = patients[i]

        p.determineDiagnosis()
        for diagnosis in p.pDiagnosis:
            if diagnosis.agent.name == disease:
                diagnosis.score = 1.0
            else:
                diagnosis.score = 0.0
        p.determinePreventionMethods(500)#90000)
        for method in p.pMethods:
            print method.name, p.dateSeen
            if method.name == preventionMethod:
                print "Found in cycle %d" % p.dateSeen
                return

def runEvaluationDiagnosis(ontology, disease, prob_finding, decay, num_days, other_disease, prob_other, threshold):
    (patients, actual_diagnosis) = createPatients(ontology, disease, prob_finding, decay, num_days, other_disease, prob_other)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i in range(0, len(patients)):
        p = patients[i]
        p.determineDiagnosis()
        agents = []
        for diagnosis in p.pDiagnosis:
            if diagnosis.score > threshold:
                agents.append(diagnosis.agent)
        if actual_diagnosis[i].name == disease:
            if actual_diagnosis[i] not in agents:
                fn += 1
            else:
                tp += 1
        else:
            if actual_diagnosis[i] in agents:
                fp += 1
            else:
                tn += 1
        #max_prob = 0.0
        #agent = None
        #for diagnosis in p.pDiagnosis:
        #    if diagnosis.score > max_prob:
        #        max_prob = diagnosis.score
        #        agent = diagnosis.agent
        #if agent.name == disease and agent == actual_diagnosis[i]:
        #    tp += 1
        #if agent.name == disease and agent != actual_diagnosis[i]:
        #    fp += 1
        #if agent.name != disease and agent == actual_diagnosis[i]:
        #    tn += 1
        #if agent.name != disease and agent != actual_diagnosis[i]:
        #    fn += 1
    print "Sensitivity: %f" % (float(tp)/(tp+fn))
    print "Specificity: %f" % (float(tn)/(fp+tn))

if __name__ == "__main__":
    o = Ontology('test full ontology')
    o.initialize(transmissionFile, findingFile, pMethodFullFile, agentFullFile)
    runEvaluationPrevention(o, "Bubonic plague", 1, 1, 365, "Bubonic plague", 0.0, "Control of Vectors")
    #for j in range(21):
    #    i = 1.0 - j*0.05
    #    print "============== i = %f ==============" % i
    #    runEvaluationDiagnosis(o, "Pneumonic plague", 0.8, 0.9, 365, "Bubonic plague", 0.2, i)
