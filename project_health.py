#!/usr/bin/env python3
"""
Project Health Dashboard - Overview of code quality
"""

import os
import sys
from collections import defaultdict
from ai_code_analyzer import AICodeAnalyzer, ProblemSeverity

def analyze_project_health(directory: str = "."):
    """Generate a project health report"""
    analyzer = AICodeAnalyzer()
    problems = analyzer.analyze_directory(directory)
    
    # Statistics
    stats = {
        'total_problems': len(problems),
        'by_severity': defaultdict(int),
        'by_type': defaultdict(int),
        'by_language': defaultdict(int),
        'files_analyzed': set(),
        'files_with_problems': set()
    }
    
    for problem in problems:
        stats['by_severity'][problem.severity.value] += 1
        stats['by_type'][problem.problem_type] += 1
        
        # Extract language from file extension
        ext = os.path.splitext(problem.file_path)[1]
        lang_map = {
            '.py': 'Python',
            '.js': 'JavaScript', 
            '.ts': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.go': 'Go',
            '.rs': 'Rust',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.cs': 'C#',
            '.swift': 'Swift',
            '.kt': 'Kotlin'
        }
        language = lang_map.get(ext, 'Other')
        stats['by_language'][language] += 1
        
        stats['files_analyzed'].add(problem.file_path)
        if problem.severity != ProblemSeverity.LOW or problem.problem_type != 'empty_file':
            stats['files_with_problems'].add(problem.file_path)
    
    return stats, problems

def calculate_health_score(stats):
    """Calculate project health score (0-100)"""
    total = stats['total_problems']
    if total == 0:
        return 100
    
    # Weight by severity
    weighted_score = (
        stats['by_severity']['critical'] * 10 +
        stats['by_severity']['high'] * 5 +
        stats['by_severity']['medium'] * 2 +
        stats['by_severity']['low'] * 1
    )
    
    # Calculate score (higher weighted_score = lower health)
    max_possible = total * 10  # If all were critical
    health_score = max(0, 100 - (weighted_score / max_possible * 100))
    
    return round(health_score, 1)

def get_health_emoji(score):
    """Get emoji based on health score"""
    if score >= 90:
        return "🟢"
    elif score >= 70:
        return "🟡"
    elif score >= 50:
        return "🟠"
    else:
        return "🔴"

def print_health_report(stats, problems):
    """Print the health report"""
    health_score = calculate_health_score(stats)
    health_emoji = get_health_emoji(health_score)
    
    print("📊 PROJECT HEALTH DASHBOARD")
    print("=" * 50)
    
    print(f"\n{health_emoji} Overall Health Score: {health_score}/100")
    
    if stats['total_problems'] == 0:
        print("\n🎉 Excellent! No problems found in your codebase.")
        return
    
    print(f"\n📈 Summary:")
    print(f"   Total Problems: {stats['total_problems']}")
    print(f"   Files Analyzed: {len(stats['files_analyzed'])}")
    print(f"   Files with Problems: {len(stats['files_with_problems'])}")
    
    if stats['files_analyzed']:
        problem_rate = len(stats['files_with_problems']) / len(stats['files_analyzed']) * 100
        print(f"   Problem Rate: {problem_rate:.1f}%")
    
    print(f"\n🚨 Issues by Severity:")
    severity_order = ['critical', 'high', 'medium', 'low']
    severity_emojis = {'critical': '🚨', 'high': '🔴', 'medium': '🟡', 'low': '🔵'}
    
    for severity in severity_order:
        count = stats['by_severity'][severity]
        if count > 0:
            emoji = severity_emojis[severity]
            print(f"   {emoji} {severity.capitalize()}: {count}")
    
    print(f"\n💻 Issues by Language:")
    for language, count in sorted(stats['by_language'].items()):
        print(f"   {language}: {count}")
    
    print(f"\n🔍 Top Problem Types:")
    top_types = sorted(stats['by_type'].items(), key=lambda x: x[1], reverse=True)[:5]
    for problem_type, count in top_types:
        print(f"   {problem_type.replace('_', ' ').title()}: {count}")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    
    critical_high = stats['by_severity']['critical'] + stats['by_severity']['high']
    if critical_high > 0:
        print("   🎯 Priority: Fix critical and high severity issues first")
    
    if stats['by_type']['syntax_error'] > 0:
        print("   🔧 Fix syntax errors to ensure code can run")
    
    if stats['by_type']['missing_import'] > 0:
        print("   📦 Add missing import statements")
    
    if stats['by_type']['print_statement'] > 0:
        print("   📝 Replace print statements with proper logging")
    
    if stats['by_type']['console_log'] > 0:
        print("   🗑️  Remove console.log statements before production")

def main():
    """Main function"""
    directory = sys.argv[1] if len(sys.argv) > 1 else "."
    
    try:
        stats, problems = analyze_project_health(directory)
        print_health_report(stats, problems)
        
        # Exit with error code if there are critical/high issues
        critical_high = stats['by_severity']['critical'] + stats['by_severity']['high']
        if critical_high > 0:
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error analyzing project health: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()