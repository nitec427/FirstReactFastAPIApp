from pydantic import BaseModel

class Notes(BaseModel):
    created_date: str
    creator: str
    title: str
    bodt: str
    duration: str
    
def schema_helper(task) -> dict:
    """Helper function to make mongo query dict"""
    
    return {
        "id": str(task["_id"]),
        "Date Created": task["created_date"],
        "Creator Name": task["creator"],
        "Title": task["title"],
        "Body": task["body"],
        "Duration": task["duration"],
    }