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