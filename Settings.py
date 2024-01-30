from enum import Enum


class Settings(Enum):
    TRACK_COUNT = 500
    SECTORS_PER_TRACK = 100
    NEIGHBORING_BLOCK_WRITE_PROBABILITY = 0.3
    PROCESS_COUNT = 10
