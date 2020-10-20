class Conflict():
    """Holds conflicts that cannot be fixed by the GA
    Allows user to easily find them and manually fix them in the schedule"""
    def __init__(self, aClass, type, conflictClass=None, majorConflict=True):
        self.aClass = aClass
        self.conflictClass = conflictClass
        self.type = type
        if majorConflict:
            self.severity = "Major"
        else:
            self.severity = "Minor"

    def __str__(self):
        if not self.conflictClass:  # if no conflict class then its a room conflict
            return "{} - conflict type: {} - Severity: {}".format(self.aClass, self.type, self.severity)
        else:
            return "{} - conflicts with {} - conflict type: {} - Severity: {}".format(self.aClass, self.conflictClass,
                                                                              self.type, self.severity)