import os
import requests
import json
import time
import glob

def get_request_id(api_key):
    """Get a request ID for file upload"""
    model_id = "22aaf847-853d-4f99-a8fe-dbee5b7d2267"
    url = f"https://api.prod.unitypredict.com/api/predict/initialize/{model_id}"
    headers = {
        "Authorization": f"Bearer APIKEY@{api_key}",
        "Content-type": "application/json"
    }
    
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    return response.json()["requestId"]

def upload_file(api_key, request_id, file_path):
    """Upload a file for prediction"""
    # Step 1: Get upload link and filename
    url = f"https://api.prod.unitypredict.com/api/predict/upload/{request_id}/{os.path.basename(file_path)}"
    headers = {
        "Authorization": f"Bearer APIKEY@{api_key}",
        "Content-type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    upload_data = response.json()
    upload_link = upload_data["uploadLink"]
    generated_filename = upload_data["fileName"]
    
    # Step 2: Upload the file content
    with open(file_path, 'rb') as f:
        file_content = f.read()
    
    headers = {"Content-Type": "application/octet-stream"}
    response = requests.put(upload_link, headers=headers, data=file_content)
    response.raise_for_status()
    
    return generated_filename

def check_status(api_key, request_id):
    """Check the status of a prediction request"""
    url = f"https://api.prod.unitypredict.com/api/predict/status/{request_id}"
    headers = {
        "Authorization": f"Bearer APIKEY@{api_key}",
        "Content-type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def wait_for_completion(api_key, request_id, max_attempts=30, delay=10):
    """
    Wait for the prediction to complete
    
    Args:
        api_key (str): Your UnityPredict API key
        request_id (str): The request ID to check
        max_attempts (int): Maximum number of attempts to check status
        delay (int): Delay between checks in seconds
    
    Returns:
        dict: The final response from the API
    """
    for attempt in range(max_attempts):
        response = check_status(api_key, request_id)
        
        if response["status"] == "Completed":
            return response
        elif response["status"] == "Error":
            raise Exception(f"Prediction failed: {response.get('errorMessages', 'Unknown error')}")
        
        print(f"Status: {response['status']}. Waiting {delay} seconds... (Attempt {attempt + 1}/{max_attempts})")
        time.sleep(delay)
    
    raise Exception("Prediction timed out")

def process_file(api_key, file_path, output_folder):
    """
    Process a text file using UnityPredict API and return the results.
    
    Args:
        api_key (str): Your UnityPredict API key
        file_path (str): Path to the text file
        output_folder (str): Path where output files should be saved
    """
    try:
        print(f"\nProcessing file: {os.path.basename(file_path)}")
        
        # Step 1: Get request ID
        request_id = get_request_id(api_key)
        
        # Step 2: Upload file
        generated_filename = upload_file(api_key, request_id, file_path)
        
        # Step 3: Make prediction
        url = f"https://api.prod.unitypredict.com/api/predict/22aaf847-853d-4f99-a8fe-dbee5b7d2267/{request_id}"
        headers = {
            "Authorization": f"Bearer APIKEY@{api_key}",
            "Content-type": "application/json"
        }
        
        data = {
            "RequestId": request_id,
            "InputValues": {
                "Input File": generated_filename
            },
            "desiredOutcomes": ["Transcript", "CorrectedText"]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        # Step 4: Wait for completion
        final_response = wait_for_completion(api_key, request_id)
        
        # Extract only the Transcript and CorrectedText
        simplified_response = {
            "Transcript": final_response["outcomes"]["Transcript"][0]["value"],
            "CorrectedText": final_response["outcomes"]["CorrectedText"][0]["value"]
        }
        
        # Save results to output folder
        output_file = os.path.join(output_folder, f"{os.path.splitext(os.path.basename(file_path))[0]}_results.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(simplified_response, f, indent=2)
            
        print(f"Results saved to: {output_file}")
        return simplified_response
        
    except Exception as e:
        print(f"Error processing file {os.path.basename(file_path)}: {str(e)}")
        return None

def process_folder(api_key, input_folder, output_folder):
    """
    Process all files in the input folder and save results to the output folder.
    
    Args:
        api_key (str): Your UnityPredict API key
        input_folder (str): Path to the folder containing input files
        output_folder (str): Name of the output folder to create in the same directory as input_folder
    """
    # Create output folder in the same directory as input folder
    output_path = os.path.join(os.path.dirname(input_folder), output_folder)
    os.makedirs(output_path, exist_ok=True)
    
    # Get all text and mp3 files in the input folder
    input_files = glob.glob(os.path.join(input_folder, "*.txt")) + glob.glob(os.path.join(input_folder, "*.mp3"))
    
    if not input_files:
        print(f"No .txt or .mp3 files found in {input_folder}")
        return
    
    print(f"Found {len(input_files)} files to process")
    
    # Process each file
    results = {}
    for file_path in input_files:
        result = process_file(api_key, file_path, output_path)
        if result:
            results[os.path.basename(file_path)] = result
    
    # Save summary of all results
    summary_file = os.path.join(output_path, "processing_summary.txt")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nProcessing complete. Summary saved to: {summary_file}")

def main():
    # Replace these with your actual values
    API_KEY = "174414322736952VVKI58NL"
    INPUT_FOLDER = r"F:\Cloud\Sync\Shared\AYShared\Yasaman\Work\Cedars\Lab Projects\Accent\Aditi\New folder"
    OUTPUT_FOLDER = "output"
    
    # Process all files in the input folder
    process_folder(API_KEY, INPUT_FOLDER, OUTPUT_FOLDER)

if __name__ == "__main__": #entry point of the script, if the script is run directly, the main function will be called  
    main()
