#!/usr/bin/env python3
"""
AI Code Analyzer - Detects problems in code and suggests solutions
"""

import os
import sys
import json
import ast
import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from enum import Enum


class ProblemSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class CodeProblem:
    file_path: str
    line_number: int
    column: int
    severity: ProblemSeverity
    problem_type: str
    description: str
    solution: str
    code_snippet: str


class AICodeAnalyzer:
    """Main analyzer class that detects problems and suggests solutions"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.supported_extensions = {
            '.py': self._analyze_python,
            '.js': self._analyze_javascript,
            '.ts': self._analyze_typescript,
            '.java': self._analyze_java,
            '.cpp': self._analyze_cpp,
            '.c': self._analyze_c,
            '.go': self._analyze_go,
            '.rs': self._analyze_rust,
            '.rb': self._analyze_ruby,
            '.php': self._analyze_php,
            '.cs': self._analyze_csharp,
            '.swift': self._analyze_swift,
            '.kt': self._analyze_kotlin
        }
    
    def _load_config(self, config_path: str = None) -> dict:
        """Load configuration from JSON file"""
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'analyzer_config.json')
        
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
        except Exception:
            pass  # Fall back to default config
        
        # Default configuration
        return {
            "analysis_rules": {
                "python": {"enabled": True},
                "javascript": {"enabled": True},
                "typescript": {"enabled": True},
                "java": {"enabled": True},
                "c_cpp": {"enabled": True}
            },
            "output": {
                "default_format": "text",
                "show_code_snippets": True,
                "group_by_severity": True
            }
        }
    
    def analyze_directory(self, directory_path: str) -> List[CodeProblem]:
        """Analyze all supported files in a directory"""
        problems = []
        directory = Path(directory_path)
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix in self.supported_extensions:
                try:
                    file_problems = self.analyze_file(str(file_path))
                    problems.extend(file_problems)
                except Exception as e:
                    problems.append(CodeProblem(
                        file_path=str(file_path),
                        line_number=1,
                        column=1,
                        severity=ProblemSeverity.HIGH,
                        problem_type="analysis_error",
                        description=f"Failed to analyze file: {str(e)}",
                        solution="Check file encoding and syntax",
                        code_snippet=""
                    ))
        
        return problems
    
    def analyze_file(self, file_path: str) -> List[CodeProblem]:
        """Analyze a single file"""
        path = Path(file_path)
        
        if not path.exists():
            return [CodeProblem(
                file_path=file_path,
                line_number=1,
                column=1,
                severity=ProblemSeverity.CRITICAL,
                problem_type="file_not_found",
                description="File does not exist",
                solution="Check the file path and ensure the file exists",
                code_snippet=""
            )]
        
        if path.suffix not in self.supported_extensions:
            return [CodeProblem(
                file_path=file_path,
                line_number=1,
                column=1,
                severity=ProblemSeverity.LOW,
                problem_type="unsupported_file",
                description=f"File type {path.suffix} is not supported for analysis",
                solution="Add support for this file type or skip analysis",
                code_snippet=""
            )]
        
        analyzer_func = self.supported_extensions[path.suffix]
        return analyzer_func(file_path)
    
    def _read_file_lines(self, file_path: str) -> List[str]:
        """Read file lines safely"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.readlines()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    return f.readlines()
            except Exception:
                return []
    
    def _analyze_python(self, file_path: str) -> List[CodeProblem]:
        """Analyze Python files"""
        problems = []
        lines = self._read_file_lines(file_path)
        
        if not lines:
            return [CodeProblem(
                file_path=file_path,
                line_number=1,
                column=1,
                severity=ProblemSeverity.MEDIUM,
                problem_type="empty_file",
                description="File is empty",
                solution="Add some code or remove the empty file",
                code_snippet=""
            )]
        
        # Check for syntax errors
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            ast.parse(content)
        except SyntaxError as e:
            problems.append(CodeProblem(
                file_path=file_path,
                line_number=e.lineno or 1,
                column=e.offset or 1,
                severity=ProblemSeverity.CRITICAL,
                problem_type="syntax_error",
                description=f"Syntax error: {e.msg}",
                solution="Fix the syntax error according to Python grammar rules",
                code_snippet=lines[e.lineno - 1].strip() if e.lineno and e.lineno <= len(lines) else ""
            ))
        except Exception as e:
            problems.append(CodeProblem(
                file_path=file_path,
                line_number=1,
                column=1,
                severity=ProblemSeverity.HIGH,
                problem_type="parse_error",
                description=f"Failed to parse Python file: {str(e)}",
                solution="Check file encoding and Python version compatibility",
                code_snippet=""
            ))
        
        # Check for common Python issues
        for line_num, line in enumerate(lines, 1):
            # Check for missing imports
            if re.search(r'\b(np\.|pd\.|plt\.|cv2\.)', line):
                # Check if numpy/pandas/matplotlib/opencv is imported
                content_before = '\n'.join(lines[:line_num-1])
                if 'np.' in line and not re.search(r'import\s+numpy\s+as\s+np|from\s+numpy\s+import', content_before):
                    problems.append(CodeProblem(
                        file_path=file_path,
                        line_number=line_num,
                        column=line.find('np.'),
                        severity=ProblemSeverity.HIGH,
                        problem_type="missing_import",
                        description="Using numpy (np.) without import statement",
                        solution="Add 'import numpy as np' at the top of the file",
                        code_snippet=line.strip()
                    ))
                elif 'pd.' in line and not re.search(r'import\s+pandas\s+as\s+pd|from\s+pandas\s+import', content_before):
                    problems.append(CodeProblem(
                        file_path=file_path,
                        line_number=line_num,
                        column=line.find('pd.'),
                        severity=ProblemSeverity.HIGH,
                        problem_type="missing_import",
                        description="Using pandas (pd.) without import statement",
                        solution="Add 'import pandas as pd' at the top of the file",
                        code_snippet=line.strip()
                    ))
                elif 'plt.' in line and not re.search(r'import\s+matplotlib\.pyplot\s+as\s+plt|from\s+matplotlib\s+import', content_before):
                    problems.append(CodeProblem(
                        file_path=file_path,
                        line_number=line_num,
                        column=line.find('plt.'),
                        severity=ProblemSeverity.HIGH,
                        problem_type="missing_import",
                        description="Using matplotlib (plt.) without import statement",
                        solution="Add 'import matplotlib.pyplot as plt' at the top of the file",
                        code_snippet=line.strip()
                    ))
            
            # Check for print statements (consider using logging)
            if re.search(r'\bprint\s*\(', line):
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('print'),
                    severity=ProblemSeverity.LOW,
                    problem_type="print_statement",
                    description="Using print() for output - consider using logging",
                    solution="Replace print() with appropriate logging statements",
                    code_snippet=line.strip()
                ))
            
            # Check for long lines
            if len(line.rstrip()) > 88:
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=89,
                    severity=ProblemSeverity.LOW,
                    problem_type="long_line",
                    description=f"Line too long ({len(line.rstrip())} > 88 characters)",
                    solution="Break long lines using parentheses or backslashes",
                    code_snippet=line.strip()
                ))
            
            # Check for TODO/FIXME comments
            if re.search(r'#\s*(TODO|FIXME|XXX)', line, re.IGNORECASE):
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('#'),
                    severity=ProblemSeverity.MEDIUM,
                    problem_type="todo_comment",
                    description="Found TODO/FIXME comment",
                    solution="Complete the TODO item or create a proper issue",
                    code_snippet=line.strip()
                ))
        
        return problems
    
    def _analyze_javascript(self, file_path: str) -> List[CodeProblem]:
        """Analyze JavaScript files"""
        problems = []
        lines = self._read_file_lines(file_path)
        
        if not lines:
            return [CodeProblem(
                file_path=file_path,
                line_number=1,
                column=1,
                severity=ProblemSeverity.MEDIUM,
                problem_type="empty_file",
                description="File is empty",
                solution="Add some code or remove the empty file",
                code_snippet=""
            )]
        
        for line_num, line in enumerate(lines, 1):
            # Check for console.log statements
            if 'console.log' in line:
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('console.log'),
                    severity=ProblemSeverity.LOW,
                    problem_type="console_log",
                    description="console.log statement found - consider removing for production",
                    solution="Remove console.log or use proper logging framework",
                    code_snippet=line.strip()
                ))
            
            # Check for var declarations (prefer let/const)
            if re.search(r'\bvar\s+', line):
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('var'),
                    severity=ProblemSeverity.MEDIUM,
                    problem_type="var_declaration",
                    description="Using 'var' - prefer 'let' or 'const'",
                    solution="Replace 'var' with 'let' for mutable variables or 'const' for constants",
                    code_snippet=line.strip()
                ))
            
            # Check for == instead of ===
            if re.search(r'[^=!]==(?!=)', line):
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('=='),
                    severity=ProblemSeverity.MEDIUM,
                    problem_type="loose_equality",
                    description="Using loose equality (==) - prefer strict equality (===)",
                    solution="Use === for strict equality comparison",
                    code_snippet=line.strip()
                ))
        
        return problems
    
    def _analyze_typescript(self, file_path: str) -> List[CodeProblem]:
        """Analyze TypeScript files"""
        problems = self._analyze_javascript(file_path)  # Start with JS analysis
        lines = self._read_file_lines(file_path)
        
        for line_num, line in enumerate(lines, 1):
            # Check for 'any' type usage
            if re.search(r':\s*any\b', line):
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('any'),
                    severity=ProblemSeverity.MEDIUM,
                    problem_type="any_type",
                    description="Using 'any' type - reduces type safety",
                    solution="Use specific types instead of 'any'",
                    code_snippet=line.strip()
                ))
        
        return problems
    
    def _analyze_java(self, file_path: str) -> List[CodeProblem]:
        """Analyze Java files"""
        problems = []
        lines = self._read_file_lines(file_path)
        
        for line_num, line in enumerate(lines, 1):
            # Check for System.out.println
            if 'System.out.println' in line:
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('System.out.println'),
                    severity=ProblemSeverity.LOW,
                    problem_type="system_out",
                    description="Using System.out.println - consider using logging",
                    solution="Use a logging framework like SLF4J or java.util.logging",
                    code_snippet=line.strip()
                ))
        
        return problems
    
    # Placeholder methods for other languages
    def _analyze_cpp(self, file_path: str) -> List[CodeProblem]:
        return self._analyze_c_family(file_path, "C++")
    
    def _analyze_c(self, file_path: str) -> List[CodeProblem]:
        return self._analyze_c_family(file_path, "C")
    
    def _analyze_c_family(self, file_path: str, language: str) -> List[CodeProblem]:
        """Analyze C/C++ files"""
        problems = []
        lines = self._read_file_lines(file_path)
        
        for line_num, line in enumerate(lines, 1):
            # Check for printf without includes
            if 'printf' in line and not any('#include <stdio.h>' in prev_line for prev_line in lines[:line_num-1]):
                problems.append(CodeProblem(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('printf'),
                    severity=ProblemSeverity.HIGH,
                    problem_type="missing_include",
                    description="Using printf without including stdio.h",
                    solution="Add #include <stdio.h> at the top of the file",
                    code_snippet=line.strip()
                ))
        
        return problems
    
    def _analyze_go(self, file_path: str) -> List[CodeProblem]:
        return []
    
    def _analyze_rust(self, file_path: str) -> List[CodeProblem]:
        return []
    
    def _analyze_ruby(self, file_path: str) -> List[CodeProblem]:
        return []
    
    def _analyze_php(self, file_path: str) -> List[CodeProblem]:
        return []
    
    def _analyze_csharp(self, file_path: str) -> List[CodeProblem]:
        return []
    
    def _analyze_swift(self, file_path: str) -> List[CodeProblem]:
        return []
    
    def _analyze_kotlin(self, file_path: str) -> List[CodeProblem]:
        return []


def format_output(problems: List[CodeProblem], output_format: str = "text") -> str:
    """Format the analysis results"""
    if output_format == "json":
        return json.dumps([{
            "file_path": p.file_path,
            "line_number": p.line_number,
            "column": p.column,
            "severity": p.severity.value,
            "problem_type": p.problem_type,
            "description": p.description,
            "solution": p.solution,
            "code_snippet": p.code_snippet
        } for p in problems], indent=2)
    
    # Text format
    if not problems:
        return "✅ No problems found! Your code looks good."
    
    output = []
    output.append(f"🔍 Found {len(problems)} problem(s):\n")
    
    # Group by severity
    severity_groups = {}
    for problem in problems:
        if problem.severity not in severity_groups:
            severity_groups[problem.severity] = []
        severity_groups[problem.severity].append(problem)
    
    severity_icons = {
        ProblemSeverity.CRITICAL: "🚨",
        ProblemSeverity.HIGH: "🔴",
        ProblemSeverity.MEDIUM: "🟡",
        ProblemSeverity.LOW: "🔵"
    }
    
    for severity in [ProblemSeverity.CRITICAL, ProblemSeverity.HIGH, ProblemSeverity.MEDIUM, ProblemSeverity.LOW]:
        if severity in severity_groups:
            output.append(f"\n{severity_icons[severity]} {severity.value.upper()} SEVERITY ({len(severity_groups[severity])} issues):")
            for problem in severity_groups[severity]:
                output.append(f"\n  📄 {problem.file_path}:{problem.line_number}:{problem.column}")
                output.append(f"     Problem: {problem.description}")
                output.append(f"     Solution: {problem.solution}")
                if problem.code_snippet:
                    output.append(f"     Code: {problem.code_snippet}")
                output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="AI Code Analyzer - Detect problems and suggest solutions")
    parser.add_argument("path", help="File or directory path to analyze")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--severity", choices=["low", "medium", "high", "critical"], 
                       help="Filter by minimum severity level")
    
    args = parser.parse_args()
    
    analyzer = AICodeAnalyzer()
    
    path = Path(args.path)
    if path.is_file():
        problems = analyzer.analyze_file(str(path))
    elif path.is_dir():
        problems = analyzer.analyze_directory(str(path))
    else:
        print(f"❌ Error: Path '{args.path}' does not exist")
        sys.exit(1)
    
    # Filter by severity if specified
    if args.severity:
        severity_levels = {
            "low": [ProblemSeverity.LOW, ProblemSeverity.MEDIUM, ProblemSeverity.HIGH, ProblemSeverity.CRITICAL],
            "medium": [ProblemSeverity.MEDIUM, ProblemSeverity.HIGH, ProblemSeverity.CRITICAL],
            "high": [ProblemSeverity.HIGH, ProblemSeverity.CRITICAL],
            "critical": [ProblemSeverity.CRITICAL]
        }
        problems = [p for p in problems if p.severity in severity_levels[args.severity]]
    
    output = format_output(problems, args.format)
    print(output)
    
    # Exit with non-zero code if critical or high severity problems found
    critical_or_high = [p for p in problems if p.severity in [ProblemSeverity.CRITICAL, ProblemSeverity.HIGH]]
    if critical_or_high:
        sys.exit(1)


if __name__ == "__main__":
    main()