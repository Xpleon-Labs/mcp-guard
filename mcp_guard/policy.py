from pydantic import BaseModel
from typing import List

class Policy(BaseModel):
    allowed_programs: List[str] = ["echo", "cat", "ls"]
    block_paths: List[str] = ["/etc/", "/var/", "/root/"]
    block_network_calls: bool = True
    max_timeout_ms: int = 5000
