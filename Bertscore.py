"""
BERTScore Evaluation Method:

We evaluated the semantic similarity between candidate transcriptions and a reference text using BERTScore, 
a contextual embedding-based metric that leverages pre-trained language models to assess semantic equivalence 
beyond surface-level word matching. Specifically, we employed the roberta-large model to compute precision, 
recall, and F1 scores for each candidate transcription by comparing contextualized token embeddings against 
the reference text. Statistical summaries including mean and standard deviation were calculated across all 
evaluated transcriptions to provide aggregate performance metrics for each group.
"""

from bert_score import score
import pandas as pd
from pathlib import Path

# Reference text (ground truth)
reference_1 = ["Based on the results from your endoscopy, we saw evidence of gastritis, specifically erythematous changes along the mucosa of the anterior antrum, indicating inflammation likely due to your NSAID use or possible Helicobacter pylori infection. We also found several small gastric polyps, which are generally benign, but we have sent biopsies to confirm their histopathology and rule out any dysplasia. Additionally, there was mild esophagitis seen in the lower esophagus, suggesting gastroesophageal reflux disease or GERD as a contributing factor to your symptoms. Thankfully the duodenum appeared unremarkable, with no evidence of celiac disease or ulcerations. We will review these findings in light of your symptoms and lab results, and I may recommend proton pump inhibitors or other acid-reducing medications to alleviate the inflammation we saw."]
reference_2 = ["The patient is a 62-year-old male with a history of poorly controlled type 2 diabetes mellitus, osteoporosis, hypothyroidism, hypertension, and hyperlipidemia, presenting with a 2-month history of progressive exertional dyspnea and intermittent chest discomfort. His past medical history is Stemsignificant for a prior myocardial infarction 10 years ago, for which he underwent percutaneous coronary intervention with stent placement in the left anterior descending artery. His current medications include metformin, lisinopril, and atorvastatin, though his hemoglobin A1c remains elevated at 9.4%, indicating suboptimal glycemic control. On physical examination, he has bilateral lower extremity edema and jugular venous distension with a potential pneumothorax, suggestive of right-sided heart failure. Recent laboratory workup revealed an elevated BNP and mildly impaired renal function with a creatinine level of 1.6 mg/dL, AST of 56, and Alt of 77. Given his cardiovascular risk profile and recent symptoms, he was referred for further evaluation with echocardiography and stress testing."]
reference_3 = ["This patient is a 57-year-old male with a history of IGG4 disease, Hyperkalaemia, Abdominal aortic aneurysm, here for longstanding ulcerative colitis, diagnosed in his early 20s, now complicated by pancolonic involvement and recurrent steroid dependence despite prior trials of mesalamine, azathioprine, and infliximab status post sigmoidectomy with colon to colon anastomosis and modified J pouch placement. He presents with a recent exacerbation characterized by increased stool frequency, tenesmus, and rectal bleeding, with endoscopic findings showing continuous mucosal friability and erosions extending from the rectum to the hepatic flexure. Additionally, he has a history of primary sclerosing cholangitis diagnosed three years ago, evidenced by characteristic beading and stricturing on MRCP, and is under surveillance for cholangiocarcinoma. His extraintestinal manifestations include arthralgias and intermittent episcleritis. Lab work shows mild anemia with iron deficiency, elevated CRP, and stable LFTs, although his ALP remains chronically elevated. Given the extent of disease and steroid dependence, I am considering the addition of a JAK inhibitor as well as a possible colectomy if his symptoms remain refractory."]
reference_4 = ["The patient is a 68-year-old male with a history of COPD, likely secondary to a 40-pack-year smoking history, who presented initially with progressively worsening dyspnea on exertion and intermittent wheezing over the past month. Pulmonary function testing revealed a FEV1/FVC ratio of 0.55, consistent with obstructive lung disease, and a significant reduction in DLCO, suggesting concomitant emphysematous changes. He has a baseline requirement of 2L home oxygen via nasal cannula, though he's recently needed intermittent increases to 3L, particularly at night. A recent high-resolution CT showed bilateral upper lobe predominant emphysema with apical bullae and scattered areas of bronchiectasis. His medications include tiotropium and albuterol inhalers, given a history of frequent exacerbations. No history of pulmonary hypertension or right heart failure, although echocardiography showed mild right ventricular hypertrophy, likely attributable to chronic hypoxic pulmonary vasoconstriction."]
# Folder path containing .txt files (candidates)
FOLDER_PATH = r"All Combined- WhisperX\1\Native non-MD" 

def process_text_file(file_path, reference):
    """Process a single text file and calculate BERTScore."""
    try:
        # Read the text file
        with open(file_path, 'r', encoding='utf-8') as f:
            candidate_text = f.read().strip()
        
        if not candidate_text:
            print(f"Warning: {file_path} is empty, skipping...")
            return None
        
        # Compute BERTScore
        candidate = [candidate_text]
        P, R, F1 = score(candidate, reference, lang="en", model_type="roberta-large")
        
        # Extract scalar values
        precision = P.item()
        recall = R.item()
        f1_score = F1.item()
        
        return {
            'file_name': file_path.name,
            'file_path': str(file_path),
            'precision': precision,
            'recall': recall,
            'f1_score': f1_score
        }
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


# Find all .txt files in the folder (recursively)
folder_path = Path(FOLDER_PATH)
if not folder_path.exists():
    print(f"Error: Folder path '{FOLDER_PATH}' does not exist!")
    exit(1)

txt_files = list(folder_path.rglob("*.txt"))

if not txt_files:
    print(f"No .txt files found in '{FOLDER_PATH}'")
    exit(1)

print(f"Found {len(txt_files)} .txt file(s) to process\n")

# Process each file
results = []
for txt_file in txt_files:
    print(f"Processing: {txt_file.name}...")
    result = process_text_file(txt_file, reference_1) #replace this with the reference text you want to use
    if result:
        results.append(result)

# Summary
if results:
    df_results = pd.DataFrame(results)
    
    # Calculate mean and standard deviation for all metrics
    metrics = ['precision', 'recall', 'f1_score']
    
    print(f"\n{'='*80}")
    print("Statistical Summary (Mean ± Standard Deviation):")
    print(f"{'='*80}")
    for metric in metrics:
        mean_val = df_results[metric].mean()
        std_val = df_results[metric].std()
        print(f"  {metric.capitalize()}: {mean_val:.4f} ± {std_val:.4f}")
    
    # Add summary rows to the dataframe
    summary_rows = [
        {
            'file_name': 'AVERAGE',
            'file_path': '',
            'precision': df_results['precision'].mean(),
            'recall': df_results['recall'].mean(),
            'f1_score': df_results['f1_score'].mean()
        },
        {
            'file_name': 'STANDARD_DEVIATION',
            'file_path': '',
            'precision': df_results['precision'].std(),
            'recall': df_results['recall'].std(),
            'f1_score': df_results['f1_score'].std()
        }
    ]
    
    # Create summary dataframe
    df_summary = pd.DataFrame(summary_rows)
    
    # Combine results with summary
    df_final = pd.concat([df_results, df_summary], ignore_index=True)
    
    # Save results to CSV in the same folder as input files
    output_csv = folder_path / "BERTScore_results_WhisperX.csv"
    df_final.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"\nResults saved to: {output_csv}")
    print(f"{'='*80}")
else:
    print("No results to save.")