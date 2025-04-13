# Contributing to CodeCoach AI

Thank you for your interest in contributing to CodeCoach AI! This document provides guidelines and instructions for contributing to make the process smooth and effective for everyone involved.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [How to Contribute](#how-to-contribute)
4. [Style Guidelines](#style-guidelines)
5. [Commit Messages](#commit-messages)
6. [Pull Requests](#pull-requests)
7. [For Students](#for-students)
8. [For Teachers](#for-teachers)

## Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive, and collaborative environment. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of different viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
   ```bash
   git clone https://github.com/YOUR-USERNAME/apCS-agentic-ai.git
   cd apCS-agentic-ai
   ```
3. **Add the original repository as upstream**
   ```bash
   git remote add upstream https://github.com/ndweir/apCS-agentic-ai.git
   ```
4. **Create a new branch** for your feature or bug fix
   ```bash
   git checkout -b feature/your-feature-name
   ```

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

- A clear title and description
- As much relevant information as possible
- A code sample or test case demonstrating the bug
- The expected behavior vs. actual behavior

### Suggesting Enhancements

For feature requests:

- Use a clear and descriptive title
- Provide a detailed description of the suggested enhancement
- Explain why this enhancement would be useful
- Include any relevant examples or mockups

### Code Contributions

1. **Choose an issue** to work on, or create a new one
2. **Discuss** your approach in the issue comments
3. **Implement** your changes, following the style guidelines
4. **Write tests** if applicable
5. **Update documentation** as needed
6. **Submit a pull request**

## Style Guidelines

### Python Code

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation (not tabs)
- Use docstrings for functions and classes
- Keep lines under 100 characters when possible

### HTML/CSS/JavaScript

- Use 2 spaces for indentation
- Follow semantic HTML practices
- Ensure accessibility compliance
- Comment complex sections of code

### Curriculum Content

- Follow the established JSON structure
- Use clear, concise language appropriate for high school students
- Include relevant keywords for search functionality
- Provide practical examples when possible

## Commit Messages

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests after the first line

Example:
```
Add inheritance example to Unit 9 curriculum

- Add Parent and Child class examples
- Include explanation of method overriding
- Add practice exercises

Fixes #123
```

## Pull Requests

1. **Update your fork** with the latest upstream changes
   ```bash
   git fetch upstream
   git merge upstream/main
   ```
2. **Push your branch** to your fork
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Submit a pull request** from your branch to the main repository
4. **Include in your PR description**:
   - What changes you've made
   - Why you've made them
   - Any issues that are addressed
   - Any special considerations or notes for reviewers

## For Students

We especially encourage contributions from students! Here are some tips:

- Start with small, manageable changes
- Ask questions if you're unsure about anything
- Use this as a learning opportunity
- Document what you've learned in your pull request
- Consider pairing with a classmate for more complex features

### Student-Friendly Issues

Look for issues tagged with:
- `good-first-issue`
- `beginner-friendly`
- `documentation`
- `ui-enhancement`

## For Teachers

Teachers can contribute in several valuable ways:

- Add curriculum content aligned with AP standards
- Review and improve existing content for accuracy
- Suggest features based on classroom needs
- Help with documentation and examples
- Mentor student contributors

### Curriculum Contributions

When adding curriculum content:
1. Follow the JSON structure in existing files
2. Ensure content aligns with official AP CS standards
3. Include a variety of examples and practice problems
4. Consider different learning styles in your explanations

---

Thank you for contributing to CodeCoach AI and helping Minnesota students learn computer science!
