#!/usr/bin/env python3
"""
Simple tests for the AI Code Analyzer
"""

import os
import tempfile
from ai_code_analyzer import AICodeAnalyzer, ProblemSeverity


def test_python_syntax_error():
    """Test Python syntax error detection"""
    analyzer = AICodeAnalyzer()
    
    # Create a temporary file with syntax error
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("def broken_function()\n    return 'missing colon'")
        temp_file = f.name
    
    try:
        problems = analyzer.analyze_file(temp_file)
        assert len(problems) > 0, "Should detect syntax error"
        
        syntax_errors = [p for p in problems if p.problem_type == "syntax_error"]
        assert len(syntax_errors) > 0, "Should find syntax error"
        assert syntax_errors[0].severity == ProblemSeverity.CRITICAL
        
        print("✅ Python syntax error detection test passed")
    finally:
        os.unlink(temp_file)


def test_javascript_var_detection():
    """Test JavaScript var detection"""
    analyzer = AICodeAnalyzer()
    
    # Create a temporary file with var usage
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write("var oldVariable = 'should use let or const';")
        temp_file = f.name
    
    try:
        problems = analyzer.analyze_file(temp_file)
        var_problems = [p for p in problems if p.problem_type == "var_declaration"]
        assert len(var_problems) > 0, "Should detect var usage"
        assert var_problems[0].severity == ProblemSeverity.MEDIUM
        
        print("✅ JavaScript var detection test passed")
    finally:
        os.unlink(temp_file)


def test_good_code():
    """Test that good code produces no problems"""
    analyzer = AICodeAnalyzer()
    
    # Create a temporary file with good Python code
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write('''
import logging

def good_function():
    """A well-written function."""
    logging.info("This is good code")
    return True
''')
        temp_file = f.name
    
    try:
        problems = analyzer.analyze_file(temp_file)
        # Should have no critical or high severity problems
        critical_high = [p for p in problems if p.severity in [ProblemSeverity.CRITICAL, ProblemSeverity.HIGH]]
        assert len(critical_high) == 0, f"Good code should not have critical/high problems: {critical_high}"
        
        print("✅ Good code test passed")
    finally:
        os.unlink(temp_file)


def test_unsupported_file():
    """Test unsupported file handling"""
    analyzer = AICodeAnalyzer()
    
    # Create a temporary file with unsupported extension
    with tempfile.NamedTemporaryFile(mode='w', suffix='.xyz', delete=False) as f:
        f.write("Some content")
        temp_file = f.name
    
    try:
        problems = analyzer.analyze_file(temp_file)
        unsupported = [p for p in problems if p.problem_type == "unsupported_file"]
        assert len(unsupported) > 0, "Should detect unsupported file"
        assert unsupported[0].severity == ProblemSeverity.LOW
        
        print("✅ Unsupported file test passed")
    finally:
        os.unlink(temp_file)


def main():
    """Run all tests"""
    print("Running AI Code Analyzer tests...\n")
    
    try:
        test_python_syntax_error()
        test_javascript_var_detection()
        test_good_code()
        test_unsupported_file()
        
        print("\n🎉 All tests passed!")
        return 0
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n💥 Test error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())