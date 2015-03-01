class Ontology(object):
	"""Ontology is the overarching class containing information
	for the bioAgent ontology"""
	def __init__(self, name):
		"""Initializes an empty ontology with the identifying name"""
		super(Ontology, self).__init__()
		self.name = name
		self.patients = {}
		self.pMethods = {}
		self.agents = {}
		self.nextPID = 1
		self.__transmissions = []
		self.__findings = []

	def addPatient(self, newPatient):
		"""Add a new patient of class Patient"""
		if newPatient.ID not in self.patients.keys():
			self.patients[self.nextPID] = newPatient
			self.nextPID += 1
		else:
			print "patient with ID {0} already in database".format(newPatient.ID)

	def addPMethod(self, newMethod):
		"""Add a new prevention method of class PMethod"""
		if newMethod.name not in self.pMethods.keys():
			self.pMethods[nawMethod.name] = newMethod
		else:
			print "method with name {0} already in database".format(newMethod.name)

	def addAgent(self, newAgent):
		"""Add a new disease agent of class Agent"""
		if newAgent.name not in self.agents.key():
			self.agents[newAgent.name] = newAgent
		else:
			print "agent with name {0} already in database".format(newAgent.name)

	def getNextPatientID(self):
		"""Get the next smallest integer as ID for patient"""
		return self.nextPID

	def loadTransmissions(self, f):
		"""Loads a list of transmissions from file"""
		pass

	def loadFindings(self, f):
		"""Loads a list of findings form file"""
		pass

	def loadPMethods(self, f):
		"""Loads a list of preventionMethods from file.
		Need to load Transmissions before loading PMethods"""

	def loadAgents(self, f):
		"""Loads a list of disease agents from file.
		Need to load Transmissions before loading Agents"""

	def __str__(self):
		return 'Ontology [{0}]: {1} patients; {2} agents; {3} prevention methods'.format(self.name, len(self.patients), len(self.agents), len(self.pMethods))

class Patient(object):
	"""Patient encodes information for a single patient"""
	def __init__(self, ID, name, dateSeen):
		"""Basic constructor to initalize all fields for the Patient class. ID, name and dateSeen
		should be given; all other fields initialized to empty set. Values can be changed directly
		by accessing class variables"""
		super(Patient, self).__init__()
		self.ID = ID
		self.name = name
		self.dateSeen = dateSeen
		self.findings = set() # A set
		self.pDiagnosis = set() # A set of probable diagnoses
		self.cDiagnosis = set() # A set of confirmed diagnoses
		self.pMethods = set() # A set of received prevention methods

	def __str__(self):
		return '{0} ({1}): seen on {2} with findings {3}, received {4} due to confirmed diagnosis: {5} and probable diagnosis: {6}'.format(
			self.name, self.ID, self.dateSeen, self.pMethods, self.cDiagnosis, self.pDiagnosis)

class Agent(object):
	"""Agent encodes information for a disease agent"""
	def __init__(self, name, incubationPeriod, mortality, findings, transmissions):
		super(Agent, self).__init__()
		self.name = name
		self.incubationPeriod = incubationPeriod
		self.mortality = mortality
		self.transmissions = transmissions

class PMethod(object):
	"""docstring for PMethod"""
	def __init__(self, name, effectiveness):
		super(PMethod, self).__init__()
		self.name = name
		self.effectiveness = effectiveness # dict of the form {TransmissionMethod: int[0, 100]}
		self.sCost = sCost # social cost (int in [0, 100])
		self.eCost = eCost # economic cost (int in [0, 100])

class DefitionObject(object):
		"""docstring for DefitionObject"""
		def __init__(self, definition):
			super(DefitionObject, self).__init__()
			self.definition = definition
				
class TransmissionMethod(DefitionObject):
	"""TransmissionMethod encodes information for a disease transmission method."""
	def __init__(self, definition):
		super(TransmissionMethod, self).__init__(definition)

class Finding(DefitionObject):
"""Finding encodes information for a clinical finding."""
	def __init__(self, definition):
		super(Finding, self).__init__(definition)

class TriggeringFinding(Object):
"""TriggeringFinding encodes information for a clinical finding + its triggering strength."""
	def __init__(self, finding, triggeringStrength):
		super(TriggeringFinding, self).__init__()
		self.finding = finding
		self.triggeringStrength = triggeringStrength
