import random
from Process import Process
from Shared import processes


class Processor:

    def __init__(self, track_count, sectors_per_track, neighboring_block_write_probability, process_count):
        self.track_count = track_count
        self.sectors_per_track = sectors_per_track
        self.neighboring_block_write_probability = neighboring_block_write_probability
        self.process_count = process_count
        self.hard_drive_tracks = []
        self.current_block = 0
        self.time = 0

    def generate_files(self):
        file_size = 0

        for process in range(self.process_count):
            file_type = random.choice(['SMALL', 'MEDIUM', 'LARGE'])

            if file_type == 'SMALL':
                file_size = random.randint(1, 10)
            elif file_type == 'MEDIUM':
                file_size = random.randint(11, 150)
            elif file_type == 'LARGE':
                file_size = random.randint(151, 500)

            read_only = random.choice([True, False])

            blocks = []

            for block in range(file_size):
                is_successful_write = random.random() < self.neighboring_block_write_probability

                if is_successful_write:
                    file_block = self.current_block
                    self.current_block += 1
                else:
                    file_block = self.current_block + 1
                    self.current_block += 2

                blocks.append(file_block)

            processes.append(Process(process, file_type, file_size, blocks, read_only))

        return True
