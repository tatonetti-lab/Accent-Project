[README.md](https://github.com/user-attachments/files/24174221/README.md)
# Accent Analysis Project

A research project analyzing the impact of speaker accent (Native vs. Non-Native English speakers with or without medical background ) on automatic speech recognition (ASR) accuracy in medical/STEM contexts. The project evaluates transcription quality using multiple metrics including Word Error Rate (WER),Levenshtein Distance, BERTScore, and Named Entity Recognition (NER) performance.

## Overview

This project investigates how accent affects the accuracy of speech-to-text transcription systems (Whisper/WhisperX) when processing medical  content. The analysis compares performance between Native and Non-Native English speakers across different medical scenarios (STEM topics) and evaluates transcription quality using various metrics.

## Features

- **Audio Transcription**: Processes audio files using Whisper/WhisperX models via UnityPredict platform
- **Grammar Correction**: Applies grammar correction to transcriptions
- **WER Analysis**: Calculates Word Error Rate for transcriptions compared to reference texts
- **BERTScore Evaluation**: Measures semantic similarity using contextual embeddings (roberta-large model)
- **NER Analysis**: Extracts and evaluates medical named entities using spaCy models
- **Levenshtein distance Analysis**: Measures the number of single-character edits required to match the transcription with the original text.
- **Statistical Analysis**: Performs mixed-effects modeling to compare groups while accounting for participant and topic variability

## Project Structure

```
Accent/
├── EntryPoint.py              # Main engine entry point for UnityPredict
├── main.py                    # Test script for running the engine
├── config.json                # Configuration for UnityPredict deployment
├── requirements.txt            # Python dependencies
│
├── Processing Scripts/
│   ├── wer_processor_corrected.py  # WER calculation for all the STEMs 
│   ├── distance_processor.py # Edit distance calculations
│   ├── json_processor.py     # Extracts corrected text from JSON responses
│   ├── Bertscore.py        # BERTScore evaluation for STEM1- STEM4
│   ├── NER_STEM.py          # Named Entity Recognition for STEM1-STEM4
│
├── Analysis Scripts/
│   ├── Mixed_effect_Model.py       # Mixed-effects linear model analysis
│

```

## STEM Topics

The project analyzes four different medical scenarios (STEM topics):

- **STEM1**: Gastroenterology case (gastritis, GERD, endoscopy findings)
- **STEM2**: Cardiovascular case (diabetes, heart failure, myocardial infarction)
- **STEM3**: Inflammatory bowel disease case (ulcerative colitis, primary sclerosing cholangitis)
- **STEM4**: Pulmonary case (COPD, emphysema, obstructive lung disease)

## Installation

### Prerequisites

- Python 3.7+
- UnityPredict platform access (for ASR models)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Accent
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Download spaCy models:
```bash
python -m spacy download en_ner_bc5cdr_md
```

4. Configure UnityPredict:
   - Update `config.json` with your UnityPredict engine ID and API keys
   - Ensure UnityPredict platform is accessible

## Usage

### Running the Transcription Engine

```bash
python main.py
```

This will process audio files through the UnityPredict platform, transcribe them using Whisper/WhisperX, and apply grammar correction.

### WER Analysis

```python
from wer_processor_corrected import process_folder_for_WER
process_folder_for_WER("path/to/transcription/folder")
```

### BERTScore Evaluation

Run the appropriate script for each STEM topic:
```bash
python Bertscore.py  
```

### NER Analysis

Run NER extraction and evaluation:
```bash
python NER.py  # For STEM1 through STEM4

```

### Statistical Analysis

Run mixed-effects modeling:
```bash
python Mixed_effect_model.py
```

This analyzes the relationship between speaker group (Native vs. Non-Native), and Participant variation and WER, accounting for variability across participants and STEM topics.

## Dependencies

- `unitypredict-engines>=1.0.0` - UnityPredict platform integration
- `numpy` - Numerical computations
- `pandas` - Data manipulation
- `statsmodels` - Statistical modeling
- `plotly` - Interactive visualizations
- `matplotlib` - Plotting
- `scispacy>=0.5.4` - Scientific NLP
- `spacy>=3.7.0,<3.8.0` - NLP processing
- `jiwer` - Word Error Rate calculation
- `bert-score` - BERTScore evaluation
- `scikit-learn` - Machine learning utilities

## Key Metrics

### Word Error Rate (WER)
Measures transcription accuracy by comparing the number of word errors (substitutions, insertions, deletions) to the reference text.

### BERTScore
Semantic similarity metric using contextual embeddings from pre-trained language models (roberta-large). Provides precision, recall, and F1 scores.

### Named Entity Recognition (NER)
Extracts medical entities (diseases, chemicals, drugs) from transcriptions and evaluates extraction accuracy using precision, recall, and F1 scores.

## Statistical Analysis

The project uses mixed-effects linear models to:
- Compare WER between Native and Non-Native speaker groups
- Account for random effects of participants and STEM topics
- Estimate variance components for different sources of variability

Key findings from the analysis:
- Non-Native speakers show significantly higher WER than Native speakers
- STEM topics show substantial variation in baseline WER
- participant variance get smaller as the ASR model output improves
- The performance gap between groups remains relatively stable across topics

## Data Format

### Input
- Audio files: `.mp3` format
- Text files: `.txt` format (for direct transcription input)

### Output
- CSV files with WER, BERTScore, and NER metrics
- Corrected transcriptions
- Statistical model summaries

## Configuration

Edit `config.json` to configure:
- UnityPredict engine settings
- Model paths
- Temporary directory locations
- API keys and deployment parameters

## Notes

- The project uses UnityPredict platform for ASR model access
- Local testing can be done using the `unitypredict_mocktool` directory
- Reference texts for each STEM topic are hardcoded in the processing scripts
- True entity sets for NER evaluation are defined per STEM topic


## Authors
Yasman Fatapour, AI Research Data Scientist 

## Acknowledgments

- UnityPredict platform for ASR model access
- spaCy for medical NER models
- Whisper/WhisperX for speech recognition

