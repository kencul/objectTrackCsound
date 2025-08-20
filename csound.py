# Step 0: install ctcsound
import ctcsound
import sys
from pathlib import Path

'''
This module provides a class to wrap the Csound API for audio synthesis.
It initializes Csound, compiles a CSD file, and provides methods to control audio events.
'''

class csound:
    def __init__(self, directory):
        # Step 1: Create csound instance
        self.cs = ctcsound.Csound()

        # Step 2: Compile CSD from text or file
        file = directory / 'csound.csd'
        self.csd = file.read_text()
        return
    
    def initialize(self):
        # Compile the CSD
        result = self.cs.compile_csd(self.csd, 1) 

        if result != ctcsound.CSOUND_SUCCESS:
            print(f"Error compiling csd!", file=sys.stderr)
            return 1
        
        # Start the Csound performance thread so it isn't blocking
        self.csthread = ctcsound.CsoundPerformanceThread(self.cs.csound())
        print("Csound initialized successfully.")
        return 0
    
    def start(self):
        print("Starting Csound...")
        # Step 3: Start the engine    
        res = self.cs.start()
        if res is not ctcsound.CSOUND_SUCCESS:
            print("Csound failed to start!")
            exit()
        
        # Start thread
        result = self.csthread.play()

        if not self.csthread.is_running():
            print(f"Error starting Csound performance thread!", file=sys.stderr)
            return 1
        
        return 0

    def check_thread(self):
        # Check if the Csound thread is still running
        if not self.csthread.is_running():
            print("Csound thread has stopped.")
            return 1
        return 0
    
    def close_thread(self):
        self.csthread.stop()
        self.csthread.join()
        print("Csound thread closed.")
        return
    
    def event_string(self, event_string):
        # Send an event string to Csound
        self.cs.event_string(event_string)
        return
    
    def set_control_channel(self, channel_name, value):
        # Set a control channel in Csound
        self.cs.set_control_channel(channel_name, value)
        return
    
    

# sys.exit()