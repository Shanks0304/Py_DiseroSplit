import os
import time
from django.conf import settings
from pathlib import Path
import tempfile
from .functions import adjust_volume_and_save, run_additional_function
import demucs.separate
import threading
import shutil

class SubprocessThread(threading.Thread):
    def __init__(self, temp_dir_path, temp_input_file, input_file_name, input_file, final_output_dir, callback=None):
        super().__init__()
        self.temp_dir_path = temp_dir_path
        self.temp_input_file = temp_input_file
        self.input_file_name = input_file_name
        self.input_file = input_file
        self.final_output_dir = final_output_dir
        self.callback = callback
        self.result = None

    def run(self):
        # Run your subprocess command here
        demucs.separate.main(["--float32", "-d", "cpu", "--out", str(self.temp_dir_path), str(self.temp_input_file)])
        # demucs.separate.main(["--float32", "--out", str(self.temp_dir_path), str(self.temp_input_file)])
        # Simulating the work done by the thread
        print(f"Processing {self.temp_input_file} in {self.temp_dir_path}")

        # Call the callback function if it exists
        if self.callback:
            self.result = self.callback(self.input_file_name, self.input_file, self.temp_dir_path, self.final_output_dir)

def upload_to_media(uploaded_file):
    uploaded_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(uploaded_dir, exist_ok=True)
    file_path = os.path.join(uploaded_dir, uploaded_file.name)
    with open(file_path, 'wb') as destination:
        for chunk in uploaded_file.chunks():
            destination.write(chunk)
    return file_path

def isAlreadyExist(uploaded_file_name):
    final_output_dir = os.path.join(settings.MEDIA_ROOT, f"downloads/{uploaded_file_name}-Stems")
    #Check output already exists
    try:
        os.makedirs(final_output_dir)
        return True
    except FileExistsError:
        return False 

def split_audio(uploaded_file_name):
    media_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    input_file_path = os.path.join(media_path, uploaded_file_name)
    final_output_dir = os.path.join(settings.MEDIA_ROOT, f"downloads/{uploaded_file_name}-Stems")

    temp_dir_path = Path(tempfile.mkdtemp(dir=final_output_dir))
    temp_input_file = temp_dir_path / f"{uploaded_file_name}_temp.wav"
    adjust_volume_and_save(input_file_path, -10, temp_input_file)
    print(temp_input_file)

    #Start splitting process
    current_time = time.time()
    subprocess_thread = SubprocessThread(temp_dir_path=temp_dir_path, temp_input_file=temp_input_file, input_file_name = uploaded_file_name, input_file = input_file_path, final_output_dir = final_output_dir, callback=start_next_function)
    subprocess_thread.start()
    print("Thread started")
    subprocess_thread.join()
    print("Elapsed time: ", time.time() - current_time)
    return subprocess_thread.result

def start_next_function(input_file_name, input_file, temp_dir_path, final_output_dir):
    print("Next function started")
    result = run_additional_function(input_file_name, input_file, temp_dir_path, final_output_dir)
    # if result:
    #     generate_zip(os.path.basename(final_output_dir), final_output_dir)
    return result
    
def generate_zip(output_filename, dir_name):
    shutil.make_archive(output_filename, 'zip', dir_name)