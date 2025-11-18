#!/usr/bin/env python3
"""
Platform Issue Triage Tool

A command-line tool for scanning log files and identifying known errors
based on error mappings from an Excel file.
"""

import argparse
import os
import sys
from pathlib import Path
import pandas as pd
from typing import List, Tuple, Dict


class TriageTool:
    """Main class for the triage tool functionality."""
    
    def __init__(self, excel_file: str = "error_mappings.xlsx"):
        """
        Initialize the triage tool.
        
        Args:
            excel_file: Path to the Excel file containing error mappings
        """
        self.excel_file = excel_file
        self.error_mappings = {}
        
    def load_error_mappings(self) -> bool:
        """
        Load error mappings from Excel file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not os.path.exists(self.excel_file):
                print(f"Error: Excel file '{self.excel_file}' not found.")
                return False
                
            # Read Excel file
            df = pd.read_excel(self.excel_file, engine='openpyxl')
            
            # Validate columns
            if len(df.columns) < 2:
                print(f"Error: Excel file must have at least 2 columns (Error Text, Interpretation).")
                return False
                
            # Use first two columns regardless of their names
            error_col = df.columns[0]
            interp_col = df.columns[1]
            
            # Build error mappings dictionary (case-insensitive keys)
            for index, row in df.iterrows():
                error_text = str(row[error_col]).strip()
                interpretation = str(row[interp_col]).strip()
                
                if error_text and error_text.lower() != 'nan':
                    self.error_mappings[error_text.lower()] = {
                        'original': error_text,
                        'interpretation': interpretation
                    }
            
            if not self.error_mappings:
                print("Warning: No valid error mappings found in Excel file.")
                return False
                
            print(f"Loaded {len(self.error_mappings)} error mappings from '{self.excel_file}'")
            return True
            
        except Exception as e:
            print(f"Error loading Excel file: {e}")
            return False
    
    def scan_log_file(self, log_file_path: str) -> List[Tuple[int, str, str]]:
        """
        Scan log file for known errors.
        
        Args:
            log_file_path: Path to the log file to scan
            
        Returns:
            List of tuples: (line_number, log_line, interpretation)
        """
        matches = []
        
        try:
            if not os.path.exists(log_file_path):
                print(f"Error: Log file '{log_file_path}' not found.")
                return matches
                
            file_size = os.path.getsize(log_file_path)
            if file_size == 0:
                print("Warning: Log file is empty.")
                return matches
                
            print(f"Scanning log file: {log_file_path} ({file_size:,} bytes)")
            
            with open(log_file_path, 'r', encoding='utf-8', errors='ignore') as file:
                for line_num, line in enumerate(file, 1):
                    line_lower = line.lower().strip()
                    
                    # Check each error mapping
                    for error_key, error_data in self.error_mappings.items():
                        if error_key in line_lower:
                            matches.append((
                                line_num,
                                line.strip(),
                                error_data['interpretation']
                            ))
                            
                    # Progress indicator for large files
                    if line_num % 10000 == 0:
                        print(f"Processed {line_num:,} lines...", end='\r')
                        
        except Exception as e:
            print(f"Error reading log file: {e}")
            
        return matches
    
    def display_results(self, matches: List[Tuple[int, str, str]], max_errors: int = None) -> None:
        """
        Display scan results in a formatted manner.
        
        Args:
            matches: List of tuples containing match information
            max_errors: Maximum number of errors to display (None for all)
        """
        if not matches:
            print("\nNo known errors detected in the log file.")
            return
            
        # Limit the number of errors to display if specified
        display_matches = matches[:max_errors] if max_errors else matches
        total_found = len(matches)
        showing = len(display_matches)
        
        print(f"\n{'='*80}")
        if max_errors and total_found > max_errors:
            print(f"TRIAGE RESULTS: Showing {showing} of {total_found} error(s) found")
        else:
            print(f"TRIAGE RESULTS: {total_found} error(s) found")
        print(f"{'='*80}")
        
        for i, (line_num, log_line, interpretation) in enumerate(display_matches, 1):
            print(f"\n[{i}] Error found at line {line_num}:")
            print(f"    Log Line: {log_line}")
            print(f"    Interpretation: {interpretation}")
            print(f"    {'-'*60}")
            
        if max_errors and total_found > max_errors:
            print(f"\n... and {total_found - max_errors} more error(s) not shown")
    
    def run_triage(self, log_file_path: str, max_errors: int = None) -> None:
        """
        Run the complete triage process.
        
        Args:
            log_file_path: Path to the log file to analyze
            max_errors: Maximum number of errors to display (None for all)
        """
        print("Platform Issue Triage Tool")
        print("=" * 40)
        
        # Load error mappings
        if not self.load_error_mappings():
            sys.exit(1)
            
        # Scan log file
        matches = self.scan_log_file(log_file_path)
        
        # Display results
        self.display_results(matches, max_errors)
        
        # Summary
        print(f"\nScan complete. Total errors found: {len(matches)}")


def main():
    """Main function to handle CLI arguments and run the triage tool."""
    parser = argparse.ArgumentParser(
        description="Platform Issue Triage Tool - Scan log files for known errors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python triage_tool.py -l /path/to/logfile.log
  python triage_tool.py -l logfile.log -e 5
  python triage_tool.py -l /var/log/app.log --excel custom_errors.xlsx -e 3
        """
    )
    
    parser.add_argument(
        '-l', '--logfile',
        required=True,
        help='Path to the log file to analyze'
    )
    
    parser.add_argument(
        '-e', '--errors',
        type=int,
        help='Maximum number of errors to display (default: show all)'
    )
    
    parser.add_argument(
        '--excel',
        default='error_mappings.xlsx',
        help='Path to Excel file with error mappings (default: error_mappings.xlsx)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Platform Triage Tool v1.0'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.errors is not None and args.errors < 1:
        print("Error: Number of errors to display must be at least 1.")
        sys.exit(1)
        
    # Initialize and run triage tool
    try:
        triage = TriageTool(excel_file=args.excel)
        triage.run_triage(args.logfile, args.errors)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()