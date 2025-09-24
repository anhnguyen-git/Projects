# AI Code Analyzer

An intelligent code analysis tool that detects problems in your code and provides actionable solutions to fix them.

## Features

🔍 **Multi-language Support**: Analyzes Python, JavaScript, TypeScript, Java, C/C++, Go, Rust, Ruby, PHP, C#, Swift, and Kotlin files

🚨 **Problem Detection**: Identifies various code issues including:
- Syntax errors
- Missing imports/includes
- Code style violations
- Security concerns
- Performance issues
- TODO/FIXME comments

💡 **Smart Solutions**: Provides specific, actionable suggestions for fixing detected problems

📊 **Severity Levels**: Categorizes issues by severity (Critical, High, Medium, Low)

🎯 **Flexible Output**: Supports both human-readable text and JSON output formats

## Quick Start

### Basic Usage

```bash
# Analyze a single file
python ai_code_analyzer.py examples/problematic_python.py

# Analyze an entire directory
python ai_code_analyzer.py examples/

# Get JSON output
python ai_code_analyzer.py examples/ --format json

# Filter by severity level
python ai_code_analyzer.py examples/ --severity high

# Use the convenient wrapper script
./analyze examples/

# Get project health overview
python project_health.py examples/

# Run the interactive demo
python demo.py
```

### Installation

No external dependencies required! The analyzer uses Python's standard library.

```bash
# Clone the repository
git clone <repository-url>
cd Projects

# Make scripts executable (optional)
chmod +x ai_code_analyzer.py analyze project_health.py demo.py

# Run analysis
python ai_code_analyzer.py <path-to-analyze>
```

## Supported Languages and Checks

### Python (.py)
- ✅ Syntax error detection
- ✅ Missing import statements
- ✅ Print statement usage (suggests logging)
- ✅ Line length violations (>88 characters)
- ✅ TODO/FIXME comment tracking
- ✅ Empty file detection

### JavaScript (.js)
- ✅ Console.log statement detection
- ✅ `var` usage (suggests `let`/`const`)
- ✅ Loose equality (`==` vs `===`)
- ✅ Empty file detection

### TypeScript (.ts)
- ✅ All JavaScript checks
- ✅ `any` type usage detection

### Java (.java)
- ✅ System.out.println detection (suggests logging)
- ✅ Empty file detection

### C/C++ (.c, .cpp)
- ✅ Missing include statements
- ✅ Empty file detection

### Other Languages
- Basic empty file and syntax checking
- Extensible architecture for adding more rules

## Example Output

```
🔍 Found 8 problem(s):

🚨 CRITICAL SEVERITY (1 issues):

  📄 examples/problematic_python.py:25:20
     Problem: Syntax error: invalid syntax
     Solution: Fix the syntax error according to Python grammar rules
     Code: def broken_function()

🔴 HIGH SEVERITY (1 issues):

  📄 examples/problematic_python.py:15:16
     Problem: Using library without import statement
     Solution: Add appropriate import statements at the top of the file
     Code: result = np.array([1, 2, 3, 4, 5])

🟡 MEDIUM SEVERITY (2 issues):

  📄 examples/problematic_python.py:12:4
     Problem: Found TODO/FIXME comment
     Solution: Complete the TODO item or create a proper issue
     Code: # TODO: Fix this function implementation

🔵 LOW SEVERITY (4 issues):

  📄 examples/problematic_python.py:13:4
     Problem: Using print() for output - consider using logging
     Solution: Replace print() with appropriate logging statements
     Code: print("Debug message")  # Should use logging instead
```

## Configuration

The analyzer can be configured using the `analyzer_config.json` file:

```json
{
  "analysis_rules": {
    "python": {
      "enabled": true,
      "rules": {
        "syntax_errors": {"enabled": true, "severity": "critical"},
        "missing_imports": {"enabled": true, "severity": "high"},
        "print_statements": {"enabled": true, "severity": "low"},
        "long_lines": {"enabled": true, "severity": "low", "max_length": 88}
      }
    }
  }
}
```

## Command Line Options

```
usage: ai_code_analyzer.py [-h] [--format {text,json}] [--severity {low,medium,high,critical}] path

positional arguments:
  path                  File or directory path to analyze

optional arguments:
  -h, --help            show this help message and exit
  --format {text,json}  Output format (default: text)
  --severity {low,medium,high,critical}
                        Filter by minimum severity level
```

## Exit Codes

- `0`: No critical or high severity issues found
- `1`: Critical or high severity issues detected

This makes the analyzer perfect for CI/CD pipelines and automated quality checks.

## Examples

The `examples/` directory contains sample code files demonstrating various issues:

- `problematic_python.py` - Python file with multiple issues
- `problematic_javascript.js` - JavaScript file with common problems
- `good_python.py` - Well-written Python code with minimal issues

## Additional Tools

### Project Health Dashboard
Get an overview of your project's code quality:
```bash
python project_health.py examples/
```

Output:
```
📊 PROJECT HEALTH DASHBOARD
==================================================

🟡 Overall Health Score: 79.5/100

📈 Summary:
   Total Problems: 20
   Files Analyzed: 2
   Files with Problems: 2

🚨 Issues by Severity:
   🚨 Critical: 1
   🔴 High: 1
   🟡 Medium: 8
   🔵 Low: 10

💡 Recommendations:
   🎯 Priority: Fix critical and high severity issues first
   🔧 Fix syntax errors to ensure code can run
```

### Interactive Demo
Run the comprehensive demo to see all features:
```bash
python demo.py
```

### CI/CD Integration
The repository includes a GitHub Actions workflow (`.github/workflows/code-analysis.yml`) that automatically runs code analysis on push and pull requests.

## Contributing

Feel free to contribute by:
1. Adding support for more programming languages
2. Implementing additional code quality checks
3. Improving existing problem detection logic
4. Adding more comprehensive test cases

## Architecture

The analyzer follows a modular design:
- `AICodeAnalyzer`: Main analysis engine
- Language-specific analyzers (`_analyze_python`, `_analyze_javascript`, etc.)
- `CodeProblem`: Data structure for representing issues
- Configurable severity levels and formatting options

## License

This project is open source and available under the MIT License.
