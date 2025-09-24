#!/usr/bin/env python3
"""
Demo script showcasing the AI Code Analyzer capabilities
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command):
    """Run a command and return its output"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode
    except Exception as e:
        return "", str(e), 1

def print_section(title):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def main():
    """Run the demo"""
    print("🤖 AI Code Analyzer Demo")
    print("This demo showcases the analyzer's capabilities")
    
    # Change to the script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    # Demo 1: Analyze problematic Python code
    print_section("1. Analyzing Problematic Python Code")
    stdout, stderr, code = run_command("python ai_code_analyzer.py examples/problematic_python.py")
    print(stdout)
    
    # Demo 2: Analyze problematic JavaScript code
    print_section("2. Analyzing Problematic JavaScript Code")
    stdout, stderr, code = run_command("python ai_code_analyzer.py examples/problematic_javascript.js")
    print(stdout)
    
    # Demo 3: Analyze good code (should show no problems)
    print_section("3. Analyzing Well-Written Code")
    stdout, stderr, code = run_command("python ai_code_analyzer.py examples/good_python.py")
    print(stdout)
    
    # Demo 4: JSON output format
    print_section("4. JSON Output Format")
    stdout, stderr, code = run_command("python ai_code_analyzer.py examples/problematic_python.py --format json")
    print(stdout[:800] + "..." if len(stdout) > 800 else stdout)
    
    # Demo 5: Severity filtering
    print_section("5. Severity Filtering (High and Critical only)")
    stdout, stderr, code = run_command("python ai_code_analyzer.py examples/problematic_python.py --severity high")
    print(stdout)
    
    # Demo 6: Directory analysis
    print_section("6. Analyzing Entire Directory")
    stdout, stderr, code = run_command("python ai_code_analyzer.py examples/ --severity medium")
    lines = stdout.split('\n')
    # Show first 30 lines to avoid too much output
    print('\n'.join(lines[:30]) + ("\n... (output truncated)" if len(lines) > 30 else ""))
    
    # Demo 7: Using the wrapper script
    print_section("7. Using the Convenient Wrapper Script")
    print("You can also use the ./analyze script:")
    print("$ ./analyze examples/good_python.py")
    stdout, stderr, code = run_command("./analyze examples/good_python.py")
    print(stdout)
    
    print("\n" + "="*60)
    print("  Demo Complete!")
    print("="*60)
    print("\nTo use the analyzer:")
    print("  python ai_code_analyzer.py <file_or_directory>")
    print("  ./analyze <file_or_directory>")
    print("\nOptions:")
    print("  --format json          Output in JSON format")
    print("  --severity <level>     Filter by severity (low, medium, high, critical)")
    print("\nFor more help:")
    print("  python ai_code_analyzer.py --help")

if __name__ == "__main__":
    main()