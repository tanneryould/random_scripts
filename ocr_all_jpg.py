import os
import argparse
from PIL import Image
import pytesseract
from datetime import datetime
from tqdm import tqdm

# Optional: Set this if tesseract is not in your PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

def log(message, verbose):
    """Helper function to print messages with timestamps when verbose is enabled."""
    if verbose:
        time_stamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{time_stamp}] {message}")

def extract_text_from_images(folder_path, output_path, verbose=False):
    jpg_files = [f for f in os.listdir(folder_path) if f.lower().endswith(".jpg")]
    total_files = len(jpg_files)
    success_count, fail_count = 0, 0
    all_text = ""

    if not jpg_files:
        print("No .jpg images found in the folder.")
        return

    log(f"Found {total_files} .jpg images to process.", verbose)

    for idx, file_name in enumerate(tqdm(sorted(jpg_files), desc="Processing images"), start=1):
        file_path = os.path.join(folder_path, file_name)
        try:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image)
            all_text += f"--- {file_name} ---\n{text.strip()}\n\n"
            success_count += 1
            log(f"[{idx}/{total_files}] Successfully processed: {file_name}", verbose)
        except Exception as e:
            fail_count += 1
            log(f"[{idx}/{total_files}] Error processing {file_name}: {e}", verbose)

    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
        log(f"Created output directory: {output_dir}", verbose)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(all_text)

    log("\nFinished processing all images.", verbose)
    log(f"Successfully processed: {success_count}", verbose)
    log(f"Failed to process: {fail_count}", verbose)
    print(f"\nAll text saved to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Batch OCR tool for JPG images.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument("-f", "--folder", type=str, help="Folder containing images (default: current directory)")
    parser.add_argument("-o", "--output", type=str, help="Output file path (default: extracted_text.txt in current directory)")
    args = parser.parse_args()

    folder_path = args.folder if args.folder else os.path.dirname(os.path.abspath(__file__))
    output_path = args.output if args.output else os.path.join(folder_path, "extracted_text.txt")

    extract_text_from_images(folder_path, output_path, verbose=args.verbose)

if __name__ == "__main__":
    main()
