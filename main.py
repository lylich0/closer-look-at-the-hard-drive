import os
from HardDrive import HardDrive
from Processor import Processor
from Shared import processes
from Settings import *


def main():
    print("Choose the maximum number of requests per second:")
    max_qps = int(input())

    execute(max_qps)


def tick():
    global next_request
    if not hard_drive.is_queue_empty():
        next_request_block = hard_drive.c_look()

        for request in hard_drive.queue:
            if request['last_queried_block'] == next_request_block:
                next_request = request

                process_index = next_request['process']
                process = processes[process_index]

                # If the quantum of time has not expired yet, execute the requests scheduled for the process during this second
                requests, request_count = hard_drive.get_request_by_process(process_index)

                # The number of quanta received per second depends on the number of processes in the queue
                process.quantum_time *= request_count

                while process.quantum_time - process.timer >= 0:
                    if requests:
                        for req in requests:
                            next_request_block = req['last_queried_block']

                            process.proceed_request(hard_drive, next_request_block)
                            requests.remove(req)

                            print(f'Process: {process_index}, Request: {req}')
                            print('\n')

                            processor.time += process.timer
                            process.timer = 0

                            hard_drive.print_queue()
                    else:
                        # If all the requests scheduled for the process in this second are completed, select the next process.
                        tick()
                        break

                if process.quantum_time - process.timer <= 0:
                    # Pending requests are scheduled to be processed in the next second.
                    processor.time += 1000
                    tick()


def execute(max_qps):
    if os.path.exists('requests.txt'):
        os.remove('requests.txt')

    if os.path.exists('time.txt'):
        os.remove('time.txt')

    queries = 0
    total_queries = 50

    while queries < total_queries:
        # The number of requests per second is distributed evenly among all processes.
        requests_per_process = max_qps // len(processes)

        for _ in range(requests_per_process):
            for process in processes:
                if queries < total_queries:
                    queries += 1
                    process.create_request(hard_drive)

    hard_drive.print_queue()
    hard_drive.read_from_file()

    while not hard_drive.is_queue_empty():
        tick()

    print(f'Total execution time: {processor.time} ms')


if __name__ == "__main__":
    hard_drive = HardDrive()

    processor = Processor(Settings.TRACK_COUNT.value, Settings.SECTORS_PER_TRACK.value, Settings.NEIGHBORING_BLOCK_WRITE_PROBABILITY.value, Settings.PROCESS_COUNT.value)
    processor.generate_files()

    main()
