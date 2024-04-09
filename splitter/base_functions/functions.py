import numpy as np
import soundfile as sf
import subprocess
import shutil
from pathlib import Path

def adjust_volume_and_save(input_file, db_change, output_file):
    data, samplerate = sf.read(input_file)
    factor = np.power(10, db_change / 20)
    adjusted_data = data * factor
    sf.write(output_file, adjusted_data, samplerate, subtype='FLOAT')
    print(f"Audio volume adjusted by {db_change}dB and saved to {output_file} in 32-bit float format.")


def run_demucs(input_file, output_dir):
    command = ['python', '-m', 'demucs.separate', '--float32', '-d', 'cpu', '--out', str(output_dir), str(input_file)]
    subprocess.run(command, check=True)
    print("Demucs processing completed with 32-bit float output.")


def invert_phase_and_mix(input_file_path, stems_files, output_file_path):
    """
    Inverts the phase of summed stems and mixes them with the original input file.
    """
    # Read the original input file
    original_data, samplerate = sf.read(input_file_path)

    # Initialize a numpy array for the sum of selected stems
    summed_stems_data = None

    # Sum the selected stems
    for stem_file in stems_files:
        data, _ = sf.read(stem_file)
        if summed_stems_data is None:
            summed_stems_data = np.zeros_like(data)
        summed_stems_data += data

    # Invert phase of the summed stems
    inverted_stems_data = summed_stems_data * -1

    # check to make sure shapes match


    error_occured = False
    # Mix inverted phase stems with the original track
    try:
        mixed_data = original_data + inverted_stems_data
        # Write the result to the output file
        sf.write(output_file_path, mixed_data, samplerate, subtype='FLOAT')
        print(f"Mixed and saved EE track to {output_file_path}")
        error_occured = False
    except ValueError:
        print(stems_files)
        print(inverted_stems_data.shape)
        print(original_data.shape)
        error_occured = True

    
    return error_occured


def run_additional_function(input_file_name, input_file, temp_dir_path, final_output_dir):
    # This will hold paths to the drums, bass, and vocals stems
    selected_stems_files = [] 
        
    # Adjusted for loop to append selected stems paths
    for stem_file in temp_dir_path.glob("**/*.wav"):
        stem_type = stem_file.stem.split('_')[-1]
        if "temp" in stem_file.stem:
            continue
        new_filename = f"{input_file_name} {stem_type.capitalize()}.wav"
        new_file_path = Path(final_output_dir) / new_filename
        adjust_volume_and_save(stem_file, 10, new_file_path)
        if stem_type in ['drums', 'bass', 'vocals']:
            selected_stems_files.append(new_file_path)      

    '''
    # Create "EE" track
    ee_output_file_path = Path(final_output_dir) / f"{input_file_name} EE.wav"
    invert_phase_and_mix(input_file, selected_stems_files, ee_output_file_path)

    # Additional step: Delete the "other" stem, if it exists
    other_stem_path = Path(final_output_dir) / f"{input_file_name} Other.wav"
    if other_stem_path.exists():
        other_stem_path.unlink()
        print(f"Deleted 'Other' stem: {other_stem_path}")
    '''
    


    try:
        # Code that may raise a PermissionError
        shutil.rmtree(temp_dir_path)  
    except PermissionError as e:
        # Handle PermissionError
        print("PermissionError:", e)
        # Optionally, perform error handling actions such as logging, notifying the user, etc.    

