import random


class Process:
    request_counter = 0

    def __init__(self, process, file_type, file_size, blocks, read_only):
        self.process = process
        self.file_type = file_type
        self.file_size = file_size
        self.blocks = blocks
        self.read_only = read_only
        self.timer = 0
        self.quantum_time = 20

    def create_request(self, hard_drive):
        # Defining the type of request
        if self.read_only:
            # If the file is open only for reading, make a reading request
            operation = 'READ'
        else:
            # Otherwise, making a request either for reading or for writing
            operation = random.choice(['READ', 'WRITE'])

        # Defining how the process will access the blocks of the file
        if self.file_type == 'LARGE':
            if random.choice([True, False]):
                query_style = 'SEQUENTIAL'
            else:
                query_style = 'RANDOM'
        else:
            query_style = 'RANDOM'

        # Determining the number of the sector from which the file begins
        last_queried_block = self.blocks[0]

        # Choosing the sector on which the operation will be performed
        if query_style == 'RANDOM':
            last_queried_block = random.choice(self.blocks)
        elif query_style == 'SEQUENTIAL':
            index_of_last_queried_block = self.blocks.index(last_queried_block)
            if index_of_last_queried_block == len(self.blocks) - 1:
                last_queried_block = self.blocks[0]
            else:
                last_queried_block = self.blocks[index_of_last_queried_block + 1]

        # Creating request
        request = {
            'request_id': Process.request_counter,
            'process': self.process,
            'query_style': query_style,
            'operation': operation,
            'last_queried_block': last_queried_block,
        }

        # Process takes 7ms to create a request
        self.timer += 7
        Process.request_counter += 1

        # Adding the request to the queue
        hard_drive.add_to_queue(request)

        # Writing the block numbers in the file
        with open('requests.txt', 'a') as file:
            file.write(str(request["last_queried_block"]) + ',')

        return f'Process: {self.process}\n{query_style}, {operation}, {last_queried_block}'

    def proceed_request(self, hard_drive, last_queried_block):
        position_time = 0

        for request in hard_drive.queue:
            if request['last_queried_block'] == last_queried_block:

                if request['operation'] == 'READ':
                    print(f'Reading from block {request["last_queried_block"]}...')
                elif request['operation'] == 'WRITE':
                    # The probability of writing to a file block is 50%
                    if random.choice([True, False]):
                        print(f'Writing to block {request["last_queried_block"]}...')
                    else:
                        print(f'Failed to write!')

                # Calculating the time it takes to move the arm
                seek_time = abs(request['last_queried_block'] // 100 - hard_drive.current_track) * 10
                position_time = seek_time + 8

                # Moving the arm
                hard_drive.current_track = request['last_queried_block'] // 100

                # Storing the time it takes to move the arm to the file
                with open('time.txt', 'a') as file:
                    file.write(str((request['request_id'], position_time)) + ',')

        # Process takes time to move the arm
        self.timer += position_time

        # Process needs 7 ms to process the result of the request
        self.timer += 7

        # Remove the completed request from the queue
        hard_drive.remove_from_queue(last_queried_block)

        return
