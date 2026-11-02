from dataclasses import dataclass
from enum import Enum
from typing import Annotated

from slimconfig import Output


class Policy(Enum):
    FIFO = "fifo"
    LRU = "lru"


class Tool(Enum):
    COMPUTE = "replay_cache"
    SAVE = "save_result"


class Task(Enum):
    RUN = "cache-trace"


@dataclass
class ComputeInput(Output):
    addresses: Annotated[list[int], "addresses"]
    sets: Annotated[int, "sets"]
    ways: Annotated[int, "ways"]
    block_size: Annotated[int, "block size"]
    policy: Annotated[Policy, "policy"]


@dataclass
class ComputeOutput(Output):
    hits: Annotated[list[bool], "hits"]
    evicted: Annotated[list[int], "evicted"]
    lines: Annotated[list[list[int]], "lines"]
    hit_count: Annotated[int, "hit count"]
    miss_count: Annotated[int, "miss count"]


@dataclass
class SaveInput(Output):
    result: Annotated[ComputeOutput, "result"]


@dataclass
class SaveOutput(Output):
    path: Annotated[str, "path"]
    result: Annotated[ComputeOutput, "result"]


TOOLS = {Tool.COMPUTE: (ComputeInput, ComputeOutput), Tool.SAVE: (SaveInput, SaveOutput)}
TASKS = {Task.RUN: (ComputeInput, SaveOutput)}
