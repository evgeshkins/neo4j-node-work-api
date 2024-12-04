from pydantic import BaseModel
from typing import List, Optional

class Relationship(BaseModel):
    id: int
    type: str
    end_node_id: int

class Node(BaseModel):
    node_id: int
    label: str
    name: Optional[str] = None
    screen_name: Optional[str] = None
    sex: Optional[int] = None
    home_town: Optional[str] = None

class NodeAndRelationships(BaseModel):
    node: Node
    relationships: List[Relationship]