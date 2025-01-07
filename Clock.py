import time

class Clock:
    _instance = None 
    
    # Ensure a single instance is created
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.clock = None
        self.start_time = time.time()
        self.elapsed_time = 0

    def update(self):
        self.elapsed_time = time.time() - self.start_time

    def get_start_time(self):
        return self.time
    
    def get_elapsed_time(self):
        return self.elapsed_time