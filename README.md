# Meeting Task Assignment System

An automated system that processes audio recordings of meetings and automatically assigns tasks to team members based on the meeting content.

## Features

- **Audio Processing**: Preprocesses audio files and converts them to text using OpenAI Whisper
- **Task Extraction**: Custom logic to identify tasks from meeting transcripts
- **Smart Assignment**: Automatically assigns tasks to team members based on:
  - Explicit name mentions
  - Role and skill matching
  - Context analysis
- **Metadata Extraction**: Extracts deadlines, priorities, dependencies, and assignment reasons
- **Tabular Output**: Displays results in a formatted table
- **PDF Export**: Automatically generates professional PDF reports with formatted tables
- **CSV Export**: Optionally saves results to CSV format

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy language model (optional, for enhanced NLP):
```bash
python -m spacy download en_core_web_sm
```

## Usage

### Basic Usage (TO RUN THE PROJECT)

```bash 
python main.py audio_file.mp3 // if the audio file is in the same folder or copy the exact path of the audio file to run.
```

### Advanced Usage

```bash
# Using this --model small brings better accuracy (small is a model of Whisper)
python main.py audio_file.wav --model small

# Save output to CSV
python main.py audio_file.m4a --output tasks.csv

# PDF is automatically generated (auto-named based on audio file)
# Or specify custom PDF name
python main.py audio_file.mp3 --pdf custom_report.pdf

# Combine options
python main.py audio_file.mp3 --model medium --output meeting_tasks.csv
```

### Supported Audio Formats

- WAV
- MP3
- M4A
- FLAC
- OGG

### Whisper Models

- `tiny`: Fastest, least accurate
- `base`: Balanced (default)
- `small`: Better accuracy   //Can be used in our project 
- `medium`: High accuracy
- `large`: Best accuracy, slowest

## Configuration

Edit `config.py` to customize:

- **Team Members**: Add/modify team members, their roles, and skills
- **Priority Keywords**: Customize priority detection patterns
- **Deadline Patterns**: Add custom deadline extraction patterns


## Technical Details

### Architecture

1. **Audio Processing** (`audio_processor.py`):
   - Preprocesses audio files
   - Uses OpenAI Whisper for Speech-to-Text conversion

2. **Task Extraction** (`task_extractor.py`):
   - Custom NLP logic for task identification
   - Pattern matching for deadlines, priorities, dependencies
   - Skill-based and role-based assignment logic

3. **Output Formatting** (`output_formatter.py`):
   - Formats results into pandas DataFrame
   - Displays formatted table in console
   - Exports to PDF (automatic, professional formatting)
   - Exports to CSV (optional)



## Requirements

- Python 3.8+
- OpenAI Whisper
- pandas
- pydub
- python-dateutil

## Notes

- The system uses custom logic for all task identification and assignment decisions
- Speech-to-Text uses OpenAI Whisper (external service, as allowed)
- Task extraction relies on pattern matching and keyword analysis
- Assignment logic matches tasks to team members based on skills, roles, and context


