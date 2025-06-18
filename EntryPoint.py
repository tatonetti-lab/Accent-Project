import os
from unitypredict_engines.Platform import ChainedInferenceRequest, ChainedInferenceResponse, FileReceivedObj, FileTransmissionObj, IPlatform, InferenceRequest, InferenceResponse, OutcomeValue
import pickle
import requests
import json
import shutil

def transcribeAudio(platform: IPlatform, audioFilePath): #calling whisper X
    platform.logMsg('Preparing to Call Whisper Model ...')

    chainedModelRequest = ChainedInferenceRequest()
    chainedModelRequest.InputValues = {
        'Audio File': FileTransmissionObj('Speech.mp3', open(audioFilePath, 'rb')),
        'Audio File Url': '',
        'Language': 'auto',
        'Format': 'txt'
    }
    chainedModelRequest.DesiredOutcomes = ['Transcription', 'Language']

    platform.logMsg('Calling Whisper Model ...')

    chainedModelResponse: ChainedInferenceResponse = platform.invokeUnityPredictModel('7d76014c-0160-4a0b-97e2-4936028b1bd9', chainedModelRequest)

    platform.logMsg('Finished Running Whisper Model ...')

    outputFile: FileReceivedObj = chainedModelResponse.Outcomes.get('Transcription')[0].get('value')

    return outputFile.LocalFilePath

def summarizeTranscript(platform: IPlatform, transcript, summaryLength):

    platform.logMsg('Calling Transcript Summarizer Model ...')

    chainedModelRequest = ChainedInferenceRequest()
    chainedModelRequest.InputValues = {
        'Transcript': transcript,
        'SummaryLength': summaryLength
    }
    chainedModelRequest.DesiredOutcomes = ['Transcription']

    chainedModelResponse: ChainedInferenceResponse = platform.invokeUnityPredictModel('dd688adf-e0d7-48b7-b562-818e0b011eca', chainedModelRequest)

    platform.logMsg('Finished Running Transcript Summarizer Model ...')

    summary: str = chainedModelResponse.Outcomes.get('Summary')[0].get('value')

    return summary

def fixGrammar(platform: IPlatform, transcript):
    platform.logMsg('Calling Grammar Correction Model ...')

    prompt = "The medical transcript below might have spelling error, if you find any correct them. Make sure not to reword the transcript. Return only the new transcript with no additional text.\n\n"
    input_message = prompt + "\n\n" + transcript

    chainedModelRequest = ChainedInferenceRequest()
    chainedModelRequest.InputValues = {
        'InputMessage': input_message,
        'InputFile': None,
        'DynamicFormResults': {},
        'EmbedInputs': {}
    }
    chainedModelRequest.DesiredOutcomes = ['OutputMessage']

    chainedModelResponse: ChainedInferenceResponse = platform.invokeUnityPredictModel('c3b7ad1a-6265-40ae-924b-e476ff46adbf', chainedModelRequest)

    platform.logMsg('Finished Running Grammar Correction Model ...')

    corrected_text: str = chainedModelResponse.Outcomes.get('OutputMessage')[0].get('value')
    return corrected_text

def run_engine(request: InferenceRequest, platform: IPlatform) -> InferenceResponse:
    platform.logMsg("Running App Engine...\n")
    engineResponse = InferenceResponse()
    
    inputFile = request.InputValues['Input File']
    localFilePath = platform.getLocalTempFolderPath() + "/input_file"
    
    # Get the file extension from the original filename
    file_extension = inputFile.split('.')[-1].lower()
    
    # Copy the file to local temp folder with appropriate extension
    localFilePath = localFilePath + "." + file_extension
    shutil.copyfileobj(platform.getRequestFile(inputFile, 'rb'), open(localFilePath, 'wb'))

    # Process based on file type
    if file_extension in ['txt', 'text']:
        # For text files, read directly and skip transcription
        with open(localFilePath, 'r') as file:
            transcription = file.read()
    else:
        # For audio files, run transcription
        transcribeFilePath = transcribeAudio(platform, localFilePath)
        with open(transcribeFilePath, "r") as file:
            transcription = file.read()

    corrected_text: str = fixGrammar(platform, transcription)

    engineResponse.Outcomes['Transcript'] = [OutcomeValue(transcription)]
    engineResponse.Outcomes['CorrectedText'] = [OutcomeValue(corrected_text)]

    platform.logMsg("Finished Running App Engine...\n")
    return engineResponse
