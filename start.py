#!/usr/bin/env python3
"""
Starter script for the bouncing ball simulation
Launches both the main window and info window
"""
import subprocess
import sys
import os
import time

def main():
    print("Starting Bouncing Ball Simulation...")
    print("Main window: 576x1024")
    print("Info window: 300x200")
    print("\nPress Ctrl+C to stop both windows\n")
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Paths to the scripts
    main_script = os.path.join(script_dir, "bouncing_ball.py")
    info_script = os.path.join(script_dir, "info_window.py")
    
    # Check if files exist
    if not os.path.exists(main_script):
        print(f"Error: {main_script} not found!")
        sys.exit(1)
    if not os.path.exists(info_script):
        print(f"Error: {info_script} not found!")
        sys.exit(1)
    
    processes = []
    
    try:
        # Start main window
        print("Launching main window...")
        main_process = subprocess.Popen([sys.executable, main_script])
        processes.append(main_process)
        
        # Small delay to let main window initialize
        time.sleep(0.5)
        
        # Start info window
        print("Launching info window...")
        info_process = subprocess.Popen([sys.executable, info_script])
        processes.append(info_process)
        
        print("\nBoth windows running!")
        print("Close either window or press Ctrl+C to exit\n")
        
        # Wait for either process to finish
        while True:
            # Check if any process has terminated
            for process in processes:
                if process.poll() is not None:
                    print("\nOne window closed. Stopping all windows...")
                    raise KeyboardInterrupt
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\nStopping simulation...")
        
        # Terminate all processes
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=2)
            except:
                process.kill()
        
        print("All windows closed. Goodbye!")

if __name__ == "__main__":
    main()
