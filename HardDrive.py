class HardDrive:
    def __init__(self):
        self.queue = []
        self.waiting_queue = []
        self.size = 0
        self.current_track = 5
        self.seek_time = 0
        self.requests = []
        self.call = 0
        self.frequency = 20

    def add_to_queue(self, request):
        # Maximum number of requests in the queue is 20
        if self.size < 20:
            self.queue.append(request)
            self.size += 1
            return True
        else:
            # If the main queue is full, block the processes
            self.waiting_queue.append(request)
            return False

    def remove_from_queue(self, last_queried_block):
        for index, request in enumerate(self.queue):
            if request['last_queried_block'] == last_queried_block:
                del self.queue[index]
                self.size -= 1
                if self.waiting_queue:
                    # Adding the first request from the blocked queue to the main queue
                    self.queue.append(self.waiting_queue.pop(0))
                    self.size += 1
                return

    def is_queue_empty(self):
        return self.size == 0

    def read_from_file(self, file_path='requests.txt'):
        with open(file_path, 'r') as file:
            content = file.read().rstrip(',')
            self.requests = [int(num) for num in content.split(',') if num.strip()]

    def fcfs(self):
        if self.requests:
            # Returning the block of the first request
            first_request = self.requests[0]
            del self.requests[0]

            return first_request

    def sstf(self):
        if self.requests:
            # Returning the block with the smallest distance to the current track
            closest_request = min(self.requests[:20], key=lambda block: abs(block // 100 - self.current_track))

            closest_request_index = self.requests.index(closest_request)
            del self.requests[closest_request_index]

            return closest_request

    def c_look(self):
        if self.requests:
            self.call += 1

            # Sorting the array for every 20 requests
            if self.call == 1 or (self.call - 1) % self.frequency == 0:
                # Sorting the requests in ascending order
                sorted_requests = sorted(self.requests[:20])

                # Finding the block with the smallest distance to the current track
                closest_request = min(sorted_requests, key=lambda block: abs(block // 100 - self.current_track))

                # Finding the query index of that block
                closest_request_index = sorted_requests.index(closest_request)

                # Dividing the requests into two lists
                forward_requests = sorted_requests[closest_request_index:]
                backward_requests = sorted_requests[:closest_request_index]

                # Combining requests in the order of movement of the disk arm
                self.requests = forward_requests + backward_requests + self.requests[20:]

            current_request = self.requests[0]
            del self.requests[0]

            return current_request

    def print_queue(self):
        if self.queue:
            print('QUEUE')
            for request in self.queue:
                print(request)
            print('\n')

    def get_request_by_process(self, process_id):
        requests = [request for request in self.queue if request['process'] == process_id]
        request_count = len(requests)
        return requests, request_count
