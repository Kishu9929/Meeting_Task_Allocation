"""
Main application entry point for Meeting Task Assignment System
"""
import sys
import argparse
from audio_processor import AudioProcessor
from task_extractor import TaskExtractor
from output_formatter import OutputFormatter


def main():
    parser = argparse.ArgumentParser(
        description="Automated Task Assignment from Meeting Audio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  python main.py audio_meeting.mp3
  python main.py audio_meeting.wav --output tasks.csv
  python main.py audio_meeting.m4a --model small
        """
    )
    
    parser.add_argument(
        "audio_file",
        type=str,
        help="Path to the input audio file"
    )
    
    parser.add_argument(
        "--model",
        type=str,
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Whisper model size (default: base)"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output CSV file path (optional)"
    )
    
    parser.add_argument(
        "--pdf",
        type=str,
        default=None,
        nargs='?',
        const="auto",
        help="Save output as PDF. Use --pdf for auto-named file or --pdf filename.pdf for custom name"
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("MEETING TASK ASSIGNMENT SYSTEM")
    print("="*80)
    print(f"\nProcessing audio file: {args.audio_file}")
    print(f"Using Whisper model: {args.model}\n")
    
    try:
        audio_processor = AudioProcessor(model_name=args.model)
        transcript = audio_processor.transcribe(args.audio_file)
        
        print("\n" + "-"*80)
        print("TRANSCRIBED TEXT:")
        print("-"*80)
        print(transcript)
        print("-"*80)

        print("\nExtracting tasks from transcript...")
        task_extractor = TaskExtractor()
        tasks = task_extractor.extract_tasks(transcript)
        
        formatter = OutputFormatter()
        formatter.display_table(tasks)
        
        if args.output:
            formatter.save_to_csv(tasks, args.output)
        
        pdf_path = None
        if args.pdf:
            if args.pdf == "auto":
                pdf_path = None  
            else:
                pdf_path = args.pdf
        else:
            pdf_path = None
        
        formatter.save_to_pdf(tasks, pdf_path, args.audio_file)
        
        print(f"\n✓ Processed {len(tasks)} tasks successfully!")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

