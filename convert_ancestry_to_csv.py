#!/usr/bin/env python3
"""
Convert AncestryDNA raw data file to CSV format
Usage: python3 convert_ancestry_to_csv.py <input_file> [output_file]
"""

import sys
import csv
import os

def convert_ancestry_to_csv(input_file, output_file=None):
    """Convert AncestryDNA txt file to CSV"""
    
    if not output_file:
        base_name = os.path.splitext(input_file)[0]
        output_file = f"{base_name}.csv"
    
    print(f"Converting: {input_file}")
    print(f"Output: {output_file}")
    
    row_count = 0
    header_lines = []
    
    with open(input_file, 'r', encoding='utf-8') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        
        # Create CSV writer
        writer = csv.writer(outfile)
        
        # Write header row
        writer.writerow(['rsid', 'chromosome', 'position', 'allele1', 'allele2'])
        
        for line in infile:
            line = line.strip()
            
            # Skip comment lines and empty lines
            if not line or line.startswith('#'):
                if line.startswith('#'):
                    header_lines.append(line)
                continue
            
            # Skip the original header line (rsid chromosome position allele1 allele2)
            if line.startswith('rsid') and 'chromosome' in line:
                continue
            
            # Split by tab (AncestryDNA is tab-delimited)
            parts = line.split('\t')
            
            # Should have 5 columns
            if len(parts) >= 5:
                writer.writerow(parts[:5])
                row_count += 1
            elif len(parts) >= 4:
                # Handle case where alleles might be combined
                writer.writerow([parts[0], parts[1], parts[2], parts[3], ''])
                row_count += 1
            
            # Progress indicator
            if row_count % 100000 == 0:
                print(f"  Processed {row_count:,} rows...")
    
    print(f"\nConversion complete!")
    print(f"Total SNPs converted: {row_count:,}")
    print(f"Output file: {output_file}")
    print(f"File size: {os.path.getsize(output_file) / (1024*1024):.2f} MB")
    
    # Print first few header lines for reference
    if header_lines:
        print(f"\nOriginal file metadata:")
        for line in header_lines[:6]:
            if line:
                print(f"  {line}")
    
    return output_file


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 convert_ancestry_to_csv.py <input_file> [output_file]")
        print("Example: python3 convert_ancestry_to_csv.py AncestryDNA.txt AncestryDNA.csv")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.exists(input_file):
        print(f"Error: File not found: {input_file}")
        sys.exit(1)
    
    convert_ancestry_to_csv(input_file, output_file)
