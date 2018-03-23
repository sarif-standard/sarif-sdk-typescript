import json

class SarifEncoder(json.JSONEncoder):
     def default(self, o):
        # do not output keys with None values
        return {k: v for k, v in o.__dict__.items() if v}


class sarifLog:

    def __init__(self):
        self.version = "1.0.0"
        self.schema = "http://json-schema.org/draft-04/schema#"
        self.runs = []


class run:

    def __init__(self):
        self.id = None
        self.stableId = None
        self.baselineId = None
        self.automationId = None
        self.architecture = None
        self.tool = None
        self.invocation = None
        self.conversion = None
        self.files = None
        self.logicalLocations = None
        self.results = None
        self.toolNotifications = None
        self.configurationNotifications = None
        self.rules = None
        self.richMessageMimeType = None
        self.properties = None

class tool:

    def __init__(self):
        self.name = None
        self.fullName = None
        self.semanticVersion = None
        self.version = None
        self.fileVersion = None
        self.language = None
        self.sarifLoggerVersion = None
        self.properties = None

class invocation:

    def __init__(self):
        self.commandLine = None
        self.responseFiles = None
        self.startTime = None
        self.endTime = None
        self.machine = None
        self.account = None
        self.processId = None
        self.fileName = None
        self.workingDirectory = None
        self.environmentVariables = None
        self.properties = None

class conversion:

    def __init__(self):
        self.tool = None
        self.invocation = None
        self.analysisToolLogFileUri = None
        self.analysisToolLogFileUriBaseId = None

class file:
    
    def __init__(self):
        self.uri = None
        self.uriBaseId = None
        self.parentKey = None
        self.offset = None
        self.length = None
        self.mimeType = None
        self.hashes = None
        self.contents = None
        self.properties = None

class hash:

    def __init__(self):
        self.value = None
        self.algorithm = None

class result:

    def __init__(self):
        self.ruleId = None
        self.ruleKey = None
        self.level = None
        self.message = None
        self.richMessage = None
        self.templatedMessage = None
        self.locations = None
        self.snippet = None
        self.toolFingerprintContribution = None
        self.codeFlows = None
        self.stacks = None
        self.relatedLocations = None
        self.suppressionStates = None
        self.baselineState = None
        self.conversionProvenance = None
        self.fixes = None
        self.properties = None

class analysisToolLogFileContents:

    def __init__(self):
        self.region = None
        self.snippet = None
        self.analysisToolLogFileUri = None
        self.analysisToolLogFileUriBaseId = None

class location:

    def __init__(self):
        self.analysisTarget = None
        self.resultFile = None
        self.fullyQualifiedLogicalName = None
        self.logicalLocationKey = None
        self.decoratedName = None
        self.properties = None

class physicalLocation:

    def __init__(self):
        self.id = None
        self.uri = None
        self.uriBaseId = None
        self.region = None

class region:

    def __init__(self):
        self.startLine = None
        self.startColumn = None
        self.endLine = None
        self.endColumn = None
        self.offset = None
        self.length = None

class logicalLocation:

    def __init__(self):
        self.name = None
        self.kind = None
        self.parentKey = None

class codeFlow:

    def __init__(self):
        self.message = None
        self.richMessage = None
        self.locations = None
        self.properties = None

class stack:

    def __init__(self):
        self.message = None
        self.richMessage = None
        self.frames = None
        self.properties = None

class stackFrame:

    def __init__(self):
        self.message = None
        self.richMessage = None
        self.physicalLocation = None
        self.module = None
        self.threadId = None
        self.fullyQualifiedLogicalName = None
        self.logicalLocationKey = None
        self.address = None
        self.offset = None
        self.parameters = None
        self.properties = None

class annotatedCodeLocation:

    def __init__(self):
        self.step = None
        self.physicalLocation = None
        self.fullyQualifiedLogicalName = None
        self.logicalLocationKey = None
        self.module = None
        self.threadId = None
        self.message = None
        self.richMessage = None
        self.kind = None
        self.target = None
        self.targetLocation = None
        self.values = None
        self.state = None
        self.targetKey = None
        self.importance = None
        self.taintKind = None
        self.snippet = None
        self.annotations = None
        self.properties = None

class annotation:

    def __init__(self):
        self.message = None
        self.richMessage = None
        self.locations = None

class rule:

    def __init__(self):
        self.id = None
        self.name = None
        self.shortDescription = None
        self.fullDescription = None
        self.richDescription = None
        self.defaultLevel = None
        self.messageTemplates = None
        self.richMessageTemplates = None
        self.helpUri = None
        self.help = None
        self.richHelp = None
        self.properties = None

class templatedMessage:

    def __init__(self):
        self.templateId = None
        self.arguments = None

class fix:

    def __init__(self):
        self.description = None
        self.richDescription = None
        self.fileChanges = None

class fileChange:

    def __init__(self):
        self.uri = None
        self.uriBaseId = None
        self.replacements = None

class replacement:

    def __init__(self):
        self.offset = None
        self.deletedLength = None
        self.insertedBytes = None

class notification:

    def __init__(self):
        self.id = None
        self.ruleId = None
        self.ruleKey = None
        self.physicalLocation = None
        self.message = None
        self.level = None
        self.threadId = None
        self.time = None
        self.exception = None
        self.properties = None

class exception:

    def __init__(self):
        self.kind = None
        self.message = None
        self.stack = None
        self.innerExceptions = None