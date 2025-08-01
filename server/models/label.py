from enum import Enum

class Label(Enum):
    Job = 'A Job Email'
    NotJob = 'Not a Job Email'
    Applied = 'Applied'
    Screening = 'Screening'
    Assessment = 'Assessment'
    InitialCall = 'InitialCall'
    Interview = 'Interview'
    Offer = 'Offer'