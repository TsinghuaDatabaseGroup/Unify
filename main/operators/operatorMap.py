"""
    Map each operator from name to its implementation class
"""
from .promptOP import promptOP
from .retrieveOP import retrieveOP
from .searchDocOP import searchDocOP
from .scanOP import scanOP
from .countOP import countOP
from .compareOP import compareOP
from .indexScanOP import indexScanOP
from .computeOP import computeOP
from .averageOP import averageOP
from .minOP import minOP
from .medianOP import medianOP
from .maxOP import maxOP
from .sumOP import sumOP
from .percentileOP import percentileOP
from .orderByOP import orderByOP
from .extractOP import extractOP
from .groupByOP import groupByOP
from .topKOP import topKOP
from .classifyOP import classifyOP
from .joinOP import joinOP
from .unionOP import unionOP
from .intersectionOP import intersectionOP
from .complementaryOP import complementaryOP
from .ratioOP import *
from .conditionalOP import ConditionalOP

OP_MAP = {
    "Scan": scanOP,
    "Filter": scanOP,
    "Compare": compareOP,
    "GroupBy":groupByOP,
    "Count": countOP,
    "Sum": sumOP,
    "Max": maxOP,
    "Min": minOP,
    "Average": averageOP,
    "Median": medianOP,
    "Percentile": percentileOP,

    "OrderBy":orderByOP,
    "Classify" : classifyOP,
    "Extract" : extractOP,
    "TopK": topKOP,

    "Join": joinOP,
    "Union": unionOP,
    "Intersection": intersectionOP,
    "Complementary": complementaryOP,
    "Compute" : computeOP,
    "Generate" : promptOP,
    "Ratio": RatioOP,
    "Conditional": ConditionalOP,

    

}

def getOPimpl(opName, index, embedModel):
    from utils.prompt import EXEC_OP_PROMPT, OP_EXPLANATION

    OP_PROMPT = EXEC_OP_PROMPT.format(opName, OP_EXPLANATION[opName])
    OPimpl = OP_MAP[opName]
    if opName == "Retrieve":
        return OPimpl(index, embedModel)
    else:
        return OPimpl(OP_PROMPT)
