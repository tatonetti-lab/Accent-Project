import json
import os
import re

def extract_corrected_text(text_content):
    """
    Extract the corrected text from a text file with JSON-like content.
    
    Args:
        text_content (str): Content of the text file
        
    Returns:
        str: The corrected text if found, empty string if not found
    """
    # Look for the CorrectedText field
    match = re.search(r'"CorrectedText":\s*"([^"]*)"', text_content, re.DOTALL)
    if match:
        return match.group(1)
    return ""

def process_json_transcript(input_file_path):
    """
    Process a text file containing JSON-like content and create a new file with the corrected text.
    
    Args:
        input_file_path (str): Path to the input text file
        
    Returns:
        str: Path to the corrected text file if successful, None if failed
    """
    try:
        # Read the text file
        with open(input_file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Extract the corrected text
        corrected_text = extract_corrected_text(content)
        
        if not corrected_text:
            print(f"Warning: No corrected text found in {input_file_path}")
            return None
        
        # Create output file path
        output_file_path = input_file_path.replace('.txt', '_corrected.txt')
        
        # Write the corrected text to a new file
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(corrected_text)
            
        print(f"Successfully created corrected file: {output_file_path}")
        return output_file_path
        
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return None

if __name__ == "__main__":
    # Example usage:
    file_path = r"results.txt"
    process_json_transcript(file_path) 