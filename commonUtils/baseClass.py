import operator

class Ontology(object):
    """Ontology is the overarching class containing information
    for the bioAgent ontology"""
    def __init__(self, name):
        """Initializes an empty ontology with the identifying name"""
        super(Ontology, self).__init__()
        self.name = name
        self.patients = {} # Dict of {ID: Patient instance}

        # Final (private) class variables to be populated by bulk
        self.__pMethods = [] # List of PMethod instances
        self.__agents = [] # List of Agent instances 
        self.__transmissions = [] # List of Transmission instances
        self.__findings = [] # List of Finding instances
 
    def addPatient(self, newPatient):
        """Add a new patient of class Patient.
        Should call initialize to load constant classes
        before adding a patient"""
        assert len(self.__pMethods), "Trying to add patient to an uninitialized ontology!"

        if newPatient.ID not in self.patients.keys():
            self.patients[newPatient.ID] = newPatient
        else:
            print "patient with ID {0} already in database".format(newPatient.ID)

    def getPatientByID(self, ID):
        """Get a patient from the ontology using his ID"""
        patient = self.patients.get(ID, None)
        if not patient:
            print "!!WARNING: Could not find patient with ID {0}".format(ID)
        return patient
 
    def getNextPatientID(self):
        """Get the next smallest unused integer as ID for patient"""
        return max([patient.ID for patient in self.patients]) + 1

    def getTransmissionByName(self, name):
        for t in self.__transmissions:
            if t.definition == name:
                return t
        
        print "!!WARNING: Could not find transmission method with definition {0}".format(name)
        return None
 
    def getFindingByName(self, name):
        for f in self.__findings:
            if f.definition == name:
                return f

        print "!!WARNING: Could not find finding with definition {0}".format(name)
        return None

    def getAgentByName(self, name):
        for a in self.__agents:
            if a.name == name:
                return a

        print "!!WARNING: Could not find agent with name {0}".format(name)
        return None

    def getPMethodByName(self, name):
        for p in self.__pMethods:
            if p.name == name:
                return p

        print "!!WARNING: Could not find pMethod with name {0}".format(name)
        return None

    def getAgentIterable(self):
        return self.__agents

    def getTransmissionMethodIterable(self):
        return self.__transmissions

    def getPreventionMethodIterable(self):
        return self.__pMethods

    def initialize(self, transmissionFile, findingFile, pMethodFile, agentFile):
        """Called to load all final classes in the ontology. Should be called
        before adding any patient!"""

        self._loadTransmissions(transmissionFile)
        self._loadFindings(findingFile)
        self._loadPMethods(pMethodFile)
        self._loadAgents(agentFile)

    def _loadTransmissions(self, filePath):
        """Loads a list of transmissions from file, file expected to
        be a single column txt file, where the single column contains
        name (aka definition) of the transmission method"""
        with open(filePath) as f:
            # f.next() # skip header
            for line in f:
                transmission = TransmissionMethod(line.rstrip())
                self.__transmissions.append(transmission)

        print "INFO: Parsed %d transmission methods" %len(self.__transmissions)

    def _loadFindings(self, filePath):
        """Loads a list of findings form file, file expected to be a
        single column txt file, where the single column contains name
        (aka definition) of the finding"""
        with open(filePath) as f:
            # f.next() # skip header
            for line in f:
                finding = Finding(line.rstrip())
                self.__findings.append(finding)

        print "INFO: Parsed %d findings" %len(self.__findings)

    def _loadPMethods(self, filePath):
        """Loads a list of preventionMethods from file.
        Need to load Transmissions before loading PMethods. 
        Expect a 5 column file:
        1. Prevention Method (may be blank due to merged line)
        2. Transmission Method
        3. Effectiveness [int, 0-100]
        4. Economic Cost [int, 0-100]
        5. Social Cost [int, 0-100]"""

        with open(filePath) as f:
            f.next() # skip header
            currentPMethod = None
            for line in f:
                data = line.rstrip().split('\t')
                assert len(data) == 5, 'expected 5 columns, got %s' %line


                (tName, eff, eCost, sCost) = (
                    data[1], int(data[2]), int(data[3]), int(data[4]))

                transmission = self.getTransmissionByName(tName)
                assert transmission is not None, "Didn't find a transmission of name %s" %(tName)

                if data[0]:
                    currentPMethod = data[0]
                    pMethod = PMethod(currentPMethod, eCost, sCost)
                    self.__pMethods.append(pMethod)
                else:
                    pMethod = self.getPMethodByName(currentPMethod)

                assert pMethod is not None, "Didn't find a pMethod to work on for the query %s :(" %currentPMethod

                pMethod.addEffectivenessForTransmission(transmission, eff)

        print "INFO: Parsed %d Prevention Methods" %len(self.__pMethods)

    def _loadAgents(self, filePath):
        """Loads a list of disease agents from file.
        Need to load Transmissions before loading Agents.
        Agents is a 5 column txt file containing:
        1. name
        2. triggering findings: comma separated list, in the form [finding]=[strength]
        3. transmissions: comma separated list
        4. reproductive number
        5. incubation period: [int]
        6. mortality: [float]"""
        with open(filePath) as f:
            f.next() #skip header
            for line in f:
                data = line.rstrip().split('\t')
                assert len(data) == 9, "Malformed data entry; expected 5 columns, got %d, %s" %(len(data), data)
                
                [name, tFindingData, transmissions, rNumber, incub, mortality, treatedMortality, stain, dose] = data 
                
                # Triggering Findings
                tFindingStrengths = [finding.split('=') for finding in tFindingData.split(',')]
                
                print tFindingStrengths

                tFindings = [TriggeringFinding(self.getFindingByName(finding), float(strength)) 
                             for [finding, strength] in tFindingStrengths]

                print "INFO: for agent %s, parsed triggering findings:" %(name)
                for tFinding in tFindings:
                    print '\t\t', tFinding
                
                # Transimssionmethod
                tMethods = [self.getTransmissionByName(transmission.strip()) for transmission in transmissions.split(',')]
                
                print "\t and transmission methods:"
                for t in tMethods:
                    print '\t\t', t

                incub = int(incub)
                mortality = float(mortality)
                rNumber = float(rNumber)

                agent = Agent(name, rNumber, incub, mortality, tFindings, tMethods)
                self.__agents.append(agent)

        print "INFO: parsed %d agents" %(len(self.__agents))


    def __str__(self):
        return 'Ontology [{0}]: {1} patients; {2} agents; {3} prevention methods'.format(self.name, len(self.patients), len(self.__agents), len(self.__pMethods))

class Patient(object):
    """Patient encodes information for a single patient"""
    def __init__(self, ontology, ID, name, dateSeen):
        """Basic constructor to initalize all fields for the Patient class. ID, name and dateSeen
        should be given; all other fields initialized to empty set. Values can be changed directly
        by accessing class variables"""
        super(Patient, self).__init__()
        self.ID = ID
        self.name = name
        self.ontology = ontology
        self.dateSeen = dateSeen
        self.findings = set() # A set
        self.pDiagnosis = set() # A set of probable diagnoses
        self.cDiagnosis = set() # A set of confirmed diagnoses
        self.pMethods = set() # A set of received prevention methods
        self.contacts = set() # Contacted

    # Setter methods
    def addFinding(self, findingName):
        finding = self.ontology.getFindingByName(findingName)
        if finding:
            self.findings.add(finding)

    def addPDiagnosis(self, agentName):
        agent = self.ontology.getAgentByName(agentName)
        if agent:
            self.pDiagnosis.add(agent)

    def addCDiagnosis(self, agentName):
        agent = self.ontology.getAgentByName(agentName)
        if agent:
            self.cDiagnosis.add(agent)

    def addContacts(self, contacts):
        self.contacts = contacts

    def __determineDiseaseScores(self):
        agents = self.ontology.getAgentIterable()
        scores = {} # Dictionary of agent to score
        max_score = 0.0
        for agent in agents:
            scores[agent] = agent.matchFindings(self.findings)
            max_score += scores[agent]
        return [Diagnosis(agent, (scores[agent]/max_score)) for agent in agents]

    def __getDiseaseScoresForContacts(self):
        scoreByDisease = {}
        for contactId in contacts:
            contact = self.ontology.getPatientByID(contactId)
            if contact is None:
                continue
            if len(contact.cDiagnosis) > 0:
                for diagnosis in contact.cDiagnosis:
                    if diagnosis not in scoreByDisease:
                        scoreByDisease[diagnosis.agent] = 0.0
                    scoreByDisease[diagnosis.agent] += 1.0
            else:
                for diagnosis in contact.pDiagnosis:
                    if diagnosis not in scoreByDisease:
                        scoreByDisease[diagnosis.agent] = 0.0
                    scoreByDisease[diagnosis.agent] += diagnosis.score
        max_score = max(scoreByDisease.iteritems(), key=operator.itemgetter(1))[1]
        for disease in scoreByDisease:
            scoreByDisease[disease] /= max_score
            scoreByDisease[disease] /= 2
            # Scores between 1.0 to 1.5
            scoreByDisease[disease] += 1
        return scoreByDisease

    def __scaleDiseaseScoresByContacts(self, scores, contactScores):
        sum_score = 0.0
        for diagnosis in scores:
            if diagnosis.agent in contactScores:
                diagnosis.score *= contactScores[diagnosis.agent]
            sum_score += diagnosis.score
        for diagnosis in scores:
            diagnosis.score /= sum_score
        return scores

    def determineDiagnosis(self):
        assert (len(self.findings)) > 0, "A diagnosis cannot be done without findings"
        scores = self.__determineDiseaseScores()
        contactScoresByDisease = self.__getDiseaseScoresForContacts()
        scores = self.__scaleDiseaseScoresByContacts(scores, contactScoresByDisease)
        self.pDiagnosis = set(scores)
        return self.pDiagnosis

    def determinePreventionMethods(self, threshold, social_weight=1.0/3, econ_weight=2.0/3):
        assert (len(self.pDiagnosis) > 0 or len(self.cDiagnosis) > 0), "Cannot determine a prevention method without a diagnosis"
        diagnoses = []
        if len(self.cDiagnosis) > 0:
            diagnoses = self.cDiagnosis
        else:
            diagnoses = self.pDiagnosis
        tMethods = self.ontology.getTransmissionMethodIterable()
        pMethods = self.ontology.getPreventionMethodIterable()
        for pMethod in pMethods:
            numerator = 0.0
            for diagnosis in diagnoses:
                for tMethod in tMethods:
                    c_k = min(30.0/diagnosis.agent.incubationPeriod, 7.0)
                    f_k = pow(diagnosis.agent.rNumber, c_k)
                    d_k = diagnosis.agent.mortality * f_k
                    numerator += diagnosis.score * diagnosis.agent.getTransmissionWeight(tMethod) \
                        * pMethod.getEffectiveNessForTMethod(tMethod) * d_k
            denominator = social_weight * pMethod.sCost + econ_weight * pMethod.eCost
            score = numerator/denominator
            if score > threshold:
                self.pMethods.add(pMethod)


    def __str__(self):
        return '{0} ({1}): seen on {2} with findings {3}, received {4} due to confirmed diagnosis: {5} and probable diagnosis: {6}'.format(
            self.name, self.ID, self.dateSeen, self.pMethods, self.cDiagnosis, self.pDiagnosis)

class Agent(object):
    """Agent encodes information for a disease agent"""
    def __init__(self, name, rNumber, incubationPeriod, mortality, findings, transmissions):
        super(Agent, self).__init__()
        self.name = name
        self.incubationPeriod = incubationPeriod
        self.rNumber = rNumber
        self.mortality = mortality 
        self.transmissions = transmissions
        self.tFindings = findings # List of TriggeringFindings

    def matchFindings(self, pFindings):
        """Given a set of findings for a patient, find the normalized score [0, 1]
        indicating how likely it is the patient is infected with this agent. """
        score = 0.0
        max_score = 0.0
        for tFinding in self.tFindings:
            max_score += tFinding.triggeringStrength
            if tFinding.finding in pFindings:
                score += tFinding.triggeringStrength
        return score/max_score

    def getTransmissionWeight(self, tMethod):
        """Get the weight of a transmission method for a given agent. To simplify, this is just 1/number of
        transmission methods (given that tMethod is one of the transmission methods for the disease)"""
        assert len(self.transmissions) > 0 % "Agent %s must have at least one transmission method" % self.name
        if tMethod in self.transmissions:
            return 1.0/len(self.transmissions)
        return 0


class PMethod(object):
    """docstring for PMethod"""
    def __init__(self, name, sCost, eCost):
        """Initiate with name(definition), social cost and economic cost,
        add in effectiveness by addEffectivenessForTransmission method"""
        super(PMethod, self).__init__()
        self.name = name
        self.effectiveness = dict() # dict of the form {TransmissionMethod: int[0, 100]}
        self.sCost = sCost # social cost (int in [0, 100])
        self.eCost = eCost # economic cost (int in [0, 100])

    def addEffectivenessForTransmission(self, transmission, effectiveness):
        self.effectiveness[transmission] = effectiveness

    def getEffectiveNessForTMethod(self, tMethod):
        assert tMethod in self.effectiveness, "No effectiveness for tMethod %s" % tMethod.definition
        return self.effectiveness[tMethod]

class DefinitionObject(object):
        """docstring for DefinitionObject"""
        def __init__(self, definition):
            super(DefinitionObject, self).__init__()
            self.definition = definition
        
        def __str__(self):
            return self.definition

class TransmissionMethod(DefinitionObject):
    """TransmissionMethod encodes information for a disease transmission method."""
    def __init__(self, definition):
        super(TransmissionMethod, self).__init__(definition)

    def __str__(self):
        return super(TransmissionMethod, self).__str__()

class Finding(DefinitionObject):
    """Finding encodes information for a clinical finding."""
    def __init__(self, definition):
        super(Finding, self).__init__(definition)

    def __str__(self):
        return super(Finding, self).__str__()
    
class TriggeringFinding(object):
    """TriggeringFinding encodes information for a clinical finding + its triggering strength."""
    def __init__(self, finding, triggeringStrength):
        super(TriggeringFinding, self).__init__()
        self.finding = finding
        self.triggeringStrength = triggeringStrength

    def __str__(self):
        return('%s: %.3f' %(self.finding.definition, self.triggeringStrength))

class Diagnosis(object):
    """Encodes a diagnosis (the agent) and the strength of the diagnosis"""
    def __init__(self, agent, score):
        super(Diagnosis, self).__init__()
        self.agent = agent
        self.score = score

    def __str__(self):
        return('%s: %.3f' %(self.agent.name, self.score))
