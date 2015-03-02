from baseClass import *

transmissionFile = '../testDataBasic/transmission_methods.txt'
findingFile = '../testDataBasic/findings.txt' 
pMethodFile = '../testDataBasic/pMethods.txt' 
agentFile= '../testDataBasic/agents.txt'

"""Basic sanity check for initializing an ontology,
using test data found in folder testDataBasic"""
o = Ontology('test ontology')
o.initialize(transmissionFile, findingFile, pMethodFile, agentFile)

print o