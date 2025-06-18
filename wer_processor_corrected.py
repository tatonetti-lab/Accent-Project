import numpy as np
from jiwer import wer
import os

def calculate_WER_STEM1(file_path1):
    stem_1_ref = "Based on the results from your endoscopy, we saw evidence of gastritis, specifically erythematous changes along the mucosa of the anterior antrum, indicating inflammation likely due to your NSAID use or possible Helicobacter pylori infection. We also found several small gastric polyps, which are generally benign, but we have sent biopsies to confirm their histopathology and rule out any dysplasia. Additionally, there was mild esophagitis seen in the lower esophagus, suggesting gastroesophageal reflux disease or GERD as a contributing factor to your symptoms. Thankfully the duodenum appeared unremarkable, with no evidence of celiac disease or ulcerations. We will review these findings in light of your symptoms and lab results, and I may recommend proton pump inhibitors or other acid-reducing medications to alleviate the inflammation we saw."
    try:
        with open(file_path1, 'r', encoding='utf-8') as file1:
            string1_hypo = file1.read().strip()
        wer_score = wer(stem_1_ref, string1_hypo)
        
        print(f"WER score between the STEM1 and Speaker: {wer_score*100:0.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")

def calculate_WER_STEM2(file_path1):
    stem_2_ref = "The patient is a 62-year-old male with a history of poorly controlled type 2 diabetes mellitus, osteoporosis, hypothyroidism, hypertension, and hyperlipidemia, presenting with a 2-month history of progressive exertional dyspnea and intermittent chest discomfort. His past medical history is significant for a prior myocardial infarction 10 years ago, for which he underwent percutaneous coronary intervention with stent placement in the left anterior descending artery. His current medications include metformin, lisinopril, and atorvastatin, though his hemoglobin A1c remains elevated at 9.4%, indicating suboptimal glycemic control. On physical examination, he has bilateral lower extremity edema and jugular venous distension with a potential pneumothorax, suggestive of right-sided heart failure. Recent laboratory workup revealed an elevated BNP and mildly impaired renal function with a creatinine level of 1.6 mg/dL, AST of 56, and Alt of 77. Given his cardiovascular risk profile and recent symptoms, he was referred for further evaluation with echocardiography and stress testing."
    try:
        with open(file_path1, 'r', encoding='utf-8') as file1:
            string2_hypo = file1.read().strip()
        wer_score = wer(stem_2_ref, string2_hypo)
        print(f"WER score between the STEM2 and Speaker: {wer_score*100:0.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")

def calculate_WER_STEM3(file_path1):
    stem_3_ref = "This patient is a 57-year-old male with a history of IGG4 disease, Hyperkalaemia, Abdominal aortic aneurysm, here for longstanding ulcerative colitis, diagnosed in his early 20s, now complicated by pancolonic involvement and recurrent steroid dependence despite prior trials of mesalamine, azathioprine, and infliximab status post sigmoidectomy with colon to colon anastomosis and modified J pouch placement. He presents with a recent exacerbation characterized by increased stool frequency, tenesmus, and rectal bleeding, with endoscopic findings showing continuous mucosal friability and erosions extending from the rectum to the hepatic flexure. Additionally, he has a history of primary sclerosing cholangitis diagnosed three years ago, evidenced by characteristic beading and stricturing on MRCP, and is under surveillance for cholangiocarcinoma. His extraintestinal manifestations include arthralgias and intermittent episcleritis. Lab work shows mild anemia with iron deficiency, elevated CRP, and stable LFTs, although his ALP remains chronically elevated. Given the extent of disease and steroid dependence, I am considering the addition of a JAK inhibitor as well as a possible colectomy if his symptoms remain refractory."
    try:
        with open(file_path1, 'r', encoding='utf-8') as file1:
            string3_hypo = file1.read().strip()
        wer_score = wer(stem_3_ref, string3_hypo)
        print(f"WER score between the STEM3 and Speaker: {wer_score*100:0.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")

def calculate_WER_STEM4(file_path1):
    stem_4_ref = "The patient is a 68-year-old male with a history of COPD, likely secondary to a 40-pack-year smoking history, who presented initially with progressively worsening dyspnea on exertion and intermittent wheezing over the past month. Pulmonary function testing revealed a FEV1/FVC ratio of 0.55, consistent with obstructive lung disease, and a significant reduction in DLCO, suggesting concomitant emphysematous changes. He has a baseline requirement of 2L home oxygen via nasal cannula, though he's recently needed intermittent increases to 3L, particularly at night. A recent high-resolution CT showed bilateral upper lobe predominant emphysema with apical bullae and scattered areas of bronchiectasis. His medications include tiotropium and albuterol inhalers, given a history of frequent exacerbations. No history of pulmonary hypertension or right heart failure, although echocardiography showed mild right ventricular hypertrophy, likely attributable to chronic hypoxic pulmonary vasoconstriction."
    try:
        with open(file_path1, 'r', encoding='utf-8') as file1:
            string4_hypo = file1.read().strip()
        wer_score = wer(stem_4_ref, string4_hypo)
        print(f"WER score between the STEM4 and Speaker: {wer_score*100:0.2f}")
    except Exception as e:
        print(f"An error occurred: {e}")

def process_folder_for_WER(folder_path):
    """
    Process all txt files in a folder and calculate WER based on filename.
    
    Args:
        folder_path (str): Path to the folder containing txt files
    """
    # Get all txt files in the folder
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
    print("Processing WER analysis for WhisperX+gpt4.......")
    
    for file_name in txt_files:
        # Get the base name without extension
        base_name = os.path.splitext(file_name)[0]
        full_path = os.path.join(folder_path, file_name)
        # actual_name = os.path.splitext(file_name)[3]
        # print(actual_name)
        # Determine which WER calculation to use based on filename
        if base_name == "1C":
            print(f"\nProcessing {file_name} with STEM1...")
            calculate_WER_STEM1(full_path)
        elif base_name == "2C":
            print(f"\nProcessing {file_name} with STEM2...")
            calculate_WER_STEM2(full_path)
        elif base_name == "3C":
            print(f"\nProcessing {file_name} with STEM3...")
            calculate_WER_STEM3(full_path)
        elif base_name == "4C":
            print(f"\nProcessing {file_name} with STEM4...")
            calculate_WER_STEM4(full_path)
        #else:
        #    print(f"\nSkipping {file_name} - filename not recognized")

if __name__ == "__main__":
    # 
    # process_folder_for_WER(r"path_to_your_folder")
    pass 

process_folder_for_WER(r"output")