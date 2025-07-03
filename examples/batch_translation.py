#!/usr/bin/env python3
"""Batch translation example for DeepL CLI"""

import subprocess
import sys
from pathlib import Path
from typing import List, Tuple
import time


def translate_file(input_path: Path, target_lang: str, output_dir: Path) -> bool:
    """
    Translate a single file
    
    Args:
        input_path: Path to input file
        target_lang: Target language code
        output_dir: Output directory
        
    Returns:
        True if successful, False otherwise
    """
    output_path = output_dir / f"{input_path.stem}_{target_lang.lower()}{input_path.suffix}"
    
    cmd = [
        "deepl-cli",
        target_lang,
        str(input_path),
        "-o", str(output_path)
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ {input_path.name} → {output_path.name}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {input_path.name}: {e.stderr.strip()}")
        return False


def check_usage() -> Tuple[int, int, float]:
    """
    Check API usage
    
    Returns:
        Tuple of (used, limit, percentage)
    """
    try:
        result = subprocess.run(
            ["deepl-cli", "--usage"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse output (this is a simplified parser)
        lines = result.stdout.strip().split('\n')
        used = limit = 0
        percentage = 0.0
        
        for line in lines:
            if "Characters used:" in line:
                used = int(line.split(':')[1].strip().replace(',', ''))
            elif "Character limit:" in line:
                limit = int(line.split(':')[1].strip().replace(',', ''))
            elif "Usage:" in line and '%' in line:
                percentage = float(line.split(':')[1].strip().replace('%', ''))
        
        return used, limit, percentage
    except:
        return 0, 0, 0.0


def main():
    """Run batch translation example"""
    print("DeepL CLI Batch Translation Example")
    print("=" * 50)
    
    # Create sample files
    sample_dir = Path("sample_documents")
    sample_dir.mkdir(exist_ok=True)
    
    # Create sample content in different languages
    samples = [
        ("english.txt", "This is a sample document in English. It contains multiple sentences for testing."),
        ("spanish.txt", "Este es un documento de muestra en español. Contiene varias oraciones para pruebas."),
        ("french.txt", "Ceci est un document exemple en français. Il contient plusieurs phrases pour les tests."),
    ]
    
    print("\nCreating sample files...")
    for filename, content in samples:
        file_path = sample_dir / filename
        file_path.write_text(content, encoding='utf-8')
        print(f"  Created: {filename}")
    
    # Target languages for translation
    target_languages = ["JA", "DE", "IT"]
    
    # Create output directory
    output_dir = Path("translated_documents")
    output_dir.mkdir(exist_ok=True)
    
    # Check initial usage
    print("\nChecking API usage before translation...")
    used_before, limit, _ = check_usage()
    
    # Perform batch translation
    print(f"\nTranslating {len(samples)} files to {len(target_languages)} languages...")
    print("-" * 50)
    
    success_count = 0
    total_count = 0
    start_time = time.time()
    
    for file_path in sample_dir.glob("*.txt"):
        for lang in target_languages:
            total_count += 1
            if translate_file(file_path, lang, output_dir):
                success_count += 1
            # Small delay to be nice to the API
            time.sleep(0.5)
    
    elapsed_time = time.time() - start_time
    
    # Check usage after translation
    print("\nChecking API usage after translation...")
    used_after, _, percentage = check_usage()
    
    # Summary
    print("\n" + "=" * 50)
    print("Translation Summary:")
    print(f"  Total files: {len(samples)}")
    print(f"  Target languages: {len(target_languages)}")
    print(f"  Total translations: {total_count}")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {total_count - success_count}")
    print(f"  Time elapsed: {elapsed_time:.1f} seconds")
    print(f"  Characters used: {used_after - used_before:,}")
    print(f"  Current usage: {percentage:.1f}%")
    
    # List output files
    print("\nOutput files:")
    for output_file in sorted(output_dir.glob("*.txt")):
        print(f"  {output_file}")
    
    # Cleanup option
    response = input("\nClean up sample and output files? (y/N): ")
    if response.lower() == 'y':
        import shutil
        shutil.rmtree(sample_dir)
        shutil.rmtree(output_dir)
        print("✓ Cleaned up")


if __name__ == "__main__":
    main()
