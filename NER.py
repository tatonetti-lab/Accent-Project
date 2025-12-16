import spacy
from sklearn.metrics import precision_recall_fscore_support
import pandas as pd
from pathlib import Path



# Medical NER model (diseases and chemicals/drugs)
nlp_medical = spacy.load("en_ner_bc5cdr_md")  # recognizes diseases and chemicals

# CRAFT model (genes, proteins, cell types, etc.)
# nlp_craft = spacy.load("en_ner_craft_md")  # recognizes genes, proteins, cell types, and other CRAFT entities

# # General biomedical models (choose one based on your needs)
# nlp_sci_md = spacy.load("en_core_sci_md")  # general biomedical entities (medium)

# print("Model loaded successfully!")

# Folder path containing .txt files
FOLDER_PATH = r"\All Combined- WhisperX\1\Non Native- Non MD"




# True entities for evaluation (can be customized per file or kept global) this is for the reference text you want to use, 
#example STEM1
true_entities = {
    "GERD",
    "Helicobacter pylori infection",
    "celiac disease",
    "dysplasia",
    "esophagitis",
    "gastritis",
    "gastroesophageal reflux disease",
    "inflammation"
}

true_entities_2 = {
    "atorvastatin",
    "creatinine",
    "diabetes mellitus",
    "dyspnea",
    "heart failure",
    "hyperlipidemia",
    "hypertension",
    "hypothyroidism",
    "jugular venous distension",
    "lisinopril",
    "lower extremity edema",
    "metformin",
    "myocardial infarction",
    "osteoporosis",
    "pneumothorax"
}

true_entities_3 = {
    "COPD", 
    "smoking", 
    "dyspnea", 
    "wheezing", 
    "obstructive lung disease", 
    "oxygen", 
    "emphysema", 
    "bronchiectasis", 
    "tiotropium", 
    "albuterol", 
    "pulmonary hypertension", 
    "right heart failure", 
    "right ventricular hypertrophy", 
    "hypertrophy",
    "Abdominal aortic aneurysm",
    "Hyperkalaemia",
    "JAK",
    "anemia",
    "arthralgias",
    "azathioprine",
    "bleeding",
    "cholangiocarcinoma",
    "colon to colon anastomosis",
    "erosions",
    "intermittent episcleritis",
    "iron deficiency",
    "mesalamine",
    "pancolonic",
    "primary sclerosing cholangitis",
    "steroid",
    "tenesmus",
    "ulcerative colitis"
}

true_entities_4 = {
    "COPD", 
    "smoking", 
    "dyspnea", 
    "wheezing", 
    "obstructive lung disease", 
    "oxygen", 
    "emphysema", 
    "bronchiectasis", 
    "tiotropium", 
    "albuterol", 
    "pulmonary hypertension", 
    "right heart failure", 
    "right ventricular hypertrophy", 
    "hypertrophy"
}

def process_text_file(file_path):
    """Process a single text file and return analysis results."""
    # print(f"\n{'='*80}")
    # print(f"Processing: {file_path}")
    # print(f"{'='*80}")
    
    # Read the text file
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None
    
    if not text.strip():
        print("File is empty, skipping...")
        return None
    
    # Process with medical NER model
    # print("\n=== Medical NER Model (en_ner_bc5cdr_md) ===")
    doc_medical = nlp_medical(text)
    
    # print("Extracted entities:")
    # for ent in doc_medical.ents:
    #     print(f"  {ent.text} - {ent.label_}")
    
    # Extract entities from medical model
    # print("\n=== Extracted Entities from Medical NER Model ===")
    combined_entities = set()
    
    # Add entities from medical model
    for ent in doc_medical.ents:
        combined_entities.add(ent.text)
    
    # print(f"\nTotal unique entities: {len(combined_entities)}")
    # for entity in sorted(combined_entities):
    #     print(f"  - {entity}")
    
    # Calculate evaluation metrics
    # print("\n=== Evaluation Metrics (Medical NER Model) ===")
    predicted_entities = combined_entities
    
    # print(f"True entities: {true_entities}")
    # print(f"Predicted entities: {predicted_entities}")
    
    tp = len(true_entities & predicted_entities)
    # print(f"\nTrue positive entities: {tp}")
    
    fp = len(predicted_entities - true_entities)
    # print(f"False positive entities: {fp}")
    
    fn = len(true_entities - predicted_entities)
    # print(f"False negative entities: {fn}")
    
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0
    
    # print(f"\nPrecision: {precision:.2f}")
    # print(f"Recall: {recall:.2f}")
    # print(f"F1 Score: {f1:.2f}")
    
    return {
        'file_path': str(file_path),
        'entities': ', '.join(sorted(combined_entities)),  # Convert set to string for CSV
        'num_entities': len(combined_entities),
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'tp': tp,
        'fp': fp,
        'fn': fn
    }


# Find all .txt files in the folder (recursively)
folder_path = Path(FOLDER_PATH)
if not folder_path.exists():
    print(f"Error: Folder path '{FOLDER_PATH}' does not exist!")
    exit(1)

txt_files = list(folder_path.rglob("*.txt"))

if not txt_files:
    print(f"No .txt files found in '{FOLDER_PATH}'")
    exit(1)

# print(f"Found {len(txt_files)} .txt file(s) to process\n")

# Process each file
results = []
for txt_file in txt_files:
    result = process_text_file(txt_file)
    if result:
        results.append(result)

# Summary
if results:
    # print(f"\n{'='*80}")
    # print("SUMMARY - All Files Processed")
    # print(f"{'='*80}")
    
    df_results = pd.DataFrame(results)
    # print("\nResults Summary:")
    # print(df_results[['file_path', 'num_entities', 'precision', 'recall', 'f1', 'tp', 'fp', 'fn']].to_string(index=False))
    
    # Calculate mean and standard deviation for all metrics
    metrics = ['num_entities', 'precision', 'recall', 'f1', 'tp', 'fp', 'fn']
    
    print(f"\n{'='*80}")
    print("Statistical Summary (Mean ± Standard Deviation):")
    print(f"{'='*80}")
    for metric in metrics:
        mean_val = df_results[metric].mean()
        std_val = df_results[metric].std()
        print(f"  {metric.capitalize()}: {mean_val:.2f} ± {std_val:.2f}")
    
    # Save results to CSV in the same folder as input files
    output_csv = folder_path / "NER_results_STEM1.csv" #replace this with the name of the reference text you want to use
    df_results.to_csv(output_csv, index=False, encoding='utf-8')
    # print(f"\n{'='*80}")
    # print(f"Results saved to: {output_csv}")
    # print(f"{'='*80}")