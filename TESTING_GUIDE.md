# Testing Guide for ARGOS

This document provides guidance on improving test coverage for the ARGOS project.

## Current Test Coverage Status
- Test files: 76
- Source files in src/: 370
- Coverage ratio: ~20.5% (below recommended 30% threshold)

## Recommendations for Improving Test Coverage

### 1. Focus on Core Modules
Prioritize testing modules in the `src/` directory that handle core functionality:
- Core systems (`src/core.py`, `src/argos_logger.py`)
- Essential skills (those loaded by default)
- Memory and knowledge systems
- Connectivity modules (P2P, MCP, etc.)

### 2. Testing Patterns to Follow
Each test file should:
- Test one specific module or functionality
- Include both positive and negative test cases
- Mock external dependencies when appropriate
- Follow the naming convention: `test_[module_name].py`

### 3. Areas Needing More Tests
Consider adding tests for:
- Configuration loading and validation
- Error handling in various modules
- Skill loading and execution workflows
- P2P communication protocols
- Memory storage and retrieval
- Plugin system functionality

### 4. Simple Test Template
```python
import unittest
from module_to_test import FunctionOrClassToTest

class TestModuleName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def tearDown(self):
        """Tear down test fixtures after each test method."""
        pass
    
    def test_function_name_normal_case(self):
        """Test normal operation of a function."""
        # Arrange
        # Act
        # Assert
        pass
    
    def test_function_name_edge_case(self):
        """Test edge cases."""
        # Arrange
        # Act
        # Assert
        pass
    
    def test_function_name_error_case(self):
        """Test error handling."""
        # Arrange
        # Act
        # Assert
        pass

if __name__ == '__main__':
    unittest.main()
```

## How to Add Tests
1. Identify a module in `src/` that lacks sufficient test coverage
2. Create a corresponding test file in `tests/` directory
3. Write tests covering the module's public interface
4. Run tests to verify they pass
5. Submit for review

## Automated Test Generation Tips
While full automation is challenging, consider:
- Using code coverage tools to identify untested lines
- Creating tests for bug fixes as they are implemented
- Adding tests for new features alongside the feature implementation
- Regularly reviewing test coverage reports

This guide aims to help increase test coverage from the current ~20.5% to the recommended 30% or higher.