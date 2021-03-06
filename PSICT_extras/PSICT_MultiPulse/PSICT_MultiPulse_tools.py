## Additional functions associated with the PSICT MultiPulse driver
## Note that some of these are used by the driver itself, so should not be edited.

import os

DEFAULT_PULSE_VALUES = {
        'a': 0.0,
        'w': 0.0,
        'v': 0.0,
        's': 0.0,
        'p': 0.0,
        'o': 4,
        ##
        'DRAG': 0.0,
        'fix_phase': 0,
        'r': 1,
        'd': 0
    }

def writePulseDefs(pPulseDefsPath, lPulseDefsIn, lPulseDefKeyOrder):
    '''
    Convenience function to quickly write the pulse definitions to file in the standardized format

    If the input is detected to have not been listified, then listifyPulseDefs will be called on it first.
    '''
    ## Preprocess path
    pPulseDefsPath = os.path.abspath(pPulseDefsPath)
    ## Create dir if it does not exist
    if not os.path.exists(os.path.dirname(pPulseDefsPath)):
        os.makedirs(os.path.dirname(pPulseDefsPath))
    ## Write key order
    with open(pPulseDefsPath, 'w') as filePulseDefs:
        filePulseDefs.write(','.join(lPulseDefKeyOrder)+'\n')
    ## If input definitions are empty, skip writing pulse definitions
    if lPulseDefsIn == []:
        pass
    elif isinstance(lPulseDefsIn[0], dict):
        ## Listify input definitions
        lPulseDefs = listifyPulseDefs(lPulseDefsIn, lPulseDefKeyOrder)
    else:
        ## Assume input definitions are already listified
        lPulseDefs = lPulseDefsIn
    ## Write pulse definitions to file
    with open(pPulseDefsPath, 'a') as filePulseDefs:
        for lPulseDef in lPulseDefs:
            filePulseDefs.write(','.join(str(quant) for quant in lPulseDef)+'\n')
    ## Return path
    return pPulseDefsPath

def writePulseSeqs(pPulseSeqsPath, lPulseSeqsIn):
    '''
    Convenience function to quickly write the pulse sequences to file in the standardized format
    '''
    ## Preprocess path
    pPulseSeqsPath = os.path.abspath(pPulseSeqsPath)
    ## Create dir if it does not exist
    if not os.path.exists(os.path.dirname(pPulseSeqsPath)):
        os.makedirs(os.path.dirname(pPulseSeqsPath))
    ## Write pulse sequences
    with open(pPulseSeqsPath, 'w') as filePulseSeq:
        for lPulseSeq in lPulseSeqsIn:
            filePulseSeq.write(','.join(str(iPulse) for iPulse in lPulseSeq)+'\n')
    ## Return path
    return pPulseSeqsPath


def listifyPulseDefs(lPulseDefsIn, lKeyOrder):
    '''
    Convert list of keyed dicts to raw definitions nested list
    '''
    lPulseDefsOut = []
    ## Cycle through each dict (corresponding to a single pulse definition)
    for oPulseDef in lPulseDefsIn:
        lPulseDef = []
        ## Populate an inner list in the specified order
        for sDefKey in lKeyOrder:
            #value = oPulseDef.get(sDefKey, DEFAULT_PULSE_VALUES[sDefKey])
            try:
                value = oPulseDef[sDefKey]
            except KeyError:
                value = DEFAULT_PULSE_VALUES[sDefKey]
            # print('Value for {} is {}'.format(sDefKey, value))
            lPulseDef.append(value)
        ## Append inner list to outer list
        lPulseDefsOut.append(lPulseDef)
    return lPulseDefsOut

def delistifyPulseDefs(lPulseDefsIn, lKeyOrder):
    '''
    Convert raw definitions nested list (pulled from file) to list of keyed dicts
    '''
    lDefsOut = []
    ## Each item in the outermost list represents a complete pulse definition
    for lDef in lPulseDefsIn:
        oDef = {}
        for dDefValue, sDefKey in zip(lDef, lKeyOrder):
            oDef[sDefKey] = dDefValue
        ## Append dict to output list
        lDefsOut.append(oDef)
    ## Return list of dicts containing keyed pulse defs
    return lDefsOut

def countNSequences(pPulseSeqsPath):
    '''
    Get the number of sequences stored in a file

    Effectively just counts the number of non-empty lines in the file.
    '''
    with open(pPulseSeqsPath, 'r') as filePulseSeq:
        iNLines = len(filePulseSeq.readlines())
    return iNLines
