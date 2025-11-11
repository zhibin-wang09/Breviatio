from enum import Enum

class EmailCategory(Enum):
    SCHEDULING = "Scheduling"
    QUESTION = "Question"
    MARKETING = "Marketing"
    JOB = "Job"
    REQUEST = "Request"
    SCHOOL = "School"
    NOTICE = "Notice"
    
    
def category_to_number(category_str: str) -> int:
    """Convert a category string (e.g. 'Marketing') to its numeric index."""
    # Normalize input (case-insensitive)
    category_str = category_str.strip().capitalize()

    # Find the matching Enum member
    for i, cat in enumerate(EmailCategory):
        if cat.value == category_str:
            return i

    # If not found, raise an error
    raise ValueError(f"Unknown category: {category_str}")