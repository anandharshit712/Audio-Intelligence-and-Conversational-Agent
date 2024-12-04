import os
import time
import subprocess
import win32serviceutil
import win32service
import win32event
import servicemanager
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Define paths and file extensions
INPUT_DIR = "Input_data"
OUTPUT_DIR = "Output_data"
SCRIPT_PATH = "main2.py"
PROCESSED_DIR = "Input_data/temp"
AUDIO_EXTENSION = ['.wav', '.mp3', '.flac', '.acc', '.m4a']

# Handler for file system events
class NewFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and self.is_audio_file(event.src_path):
            servicemanager.LogInfoMsg(f"New audio file detected: {event.src_path}")
            self.process_file(event.src_path)

    def is_audio_file(self, filepath):
        _, extention = os.path.splitext(filepath)
        return extention.lower() in AUDIO_EXTENSION

    def process_file(self, filepath):
        try:
            subprocess.run(['python', SCRIPT_PATH, filepath], check=True)
            servicemanager.LogInfoMsg(f"Processed File: {filepath}")

            if PROCESSED_DIR:
                os.makedirs(PROCESSED_DIR, exist_ok=True)
                filename = os.path.basename(filepath)
                destination = os.path.join(PROCESSED_DIR, filename)
                os.rename(filepath, destination)
                servicemanager.LogInfoMsg(f"Moved processed file to: {destination}")

        except subprocess.CalledProcessError:
            servicemanager.LogErrorMsg(f"Error Processing file {filepath}")
        except Exception as e:
            servicemanager.LogErrorMsg(f"Unexpected error: {e}")

# Main service class
class PythonWindowsService(win32serviceutil.ServiceFramework):
    _svc_name_ = "AudioFileProcessingService"
    _svc_display_name_ = "Audio File Processing Service"
    _svc_description_ = "Monitors and processes audio files in a directory."

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.running = False

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Audio File Processing Service is starting.")
        try:
            # Create output directory if it doesn't exist
            if not os.path.exists(OUTPUT_DIR):
                os.makedirs(OUTPUT_DIR)
                servicemanager.LogInfoMsg(f"Created OUTPUT_DIR: {OUTPUT_DIR}")

            # Create processed directory if it doesn't exist
            if not os.path.exists(PROCESSED_DIR):
                os.makedirs(PROCESSED_DIR)
                servicemanager.LogInfoMsg(f"Created PROCESSED_DIR: {PROCESSED_DIR}")

            # Only start the observer after confirming directories are set up
            event_handler = NewFileHandler()
            observer = Observer()
            observer.schedule(event_handler, path=INPUT_DIR, recursive=False)
            observer.start()
            servicemanager.LogInfoMsg(f"Monitoring {INPUT_DIR} for new files...")

            while self.running:
                time.sleep(1)

        except Exception as e:
            servicemanager.LogErrorMsg(f"Service encountered an error: {e}")
        finally:
            # Ensure observer is properly stopped
            observer.stop()
            observer.join()
            servicemanager.LogInfoMsg("Audio File Processing Service has stopped.")



if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(PythonWindowsService)