# CodeCoach AI: Student Learning Guide

This guide is designed for Minnesota high school students who want to learn from the CodeCoach AI codebase. Whether you're taking AP Computer Science or just interested in programming, this document will help you understand how the application works and how you can use it as a learning resource.

## Learning Opportunities

CodeCoach AI isn't just a tutoring tool - it's also a complete, real-world application that demonstrates many important computer science concepts. By studying this codebase, you can learn about:

1. **Web Development**: How web applications work from front to back
2. **Python Programming**: Real-world Python code in action
3. **Database Design**: How to store and retrieve data efficiently
4. **Search Algorithms**: How to match questions to answers
5. **User Interface Design**: Creating accessible, responsive interfaces

## Getting Started with the Code

### Prerequisites

Before diving into the code, you should have some basic knowledge of:
- Python programming
- HTML/CSS
- Basic web concepts (HTTP, browsers, servers)

Don't worry if you're still learning these - exploring the code can be part of your learning journey!

### Setting Up a Development Environment

1. **Install Python**: Download and install Python 3.8 or higher
2. **Install Git**: Download and install Git for version control
3. **Clone the Repository**:
   ```bash
   git clone https://github.com/ndweir/apCS-agentic-ai.git
   cd apCS-agentic-ai
   ```
4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
5. **Run the Application**:
   ```bash
   python app.py
   ```
6. **Open in Browser**: Visit `http://localhost:5001`

### Exploring the Code

Start by exploring these key files:

1. **app.py**: The main application file
2. **templates/index.html**: The user interface
3. **curriculum/ap_cs_a/unit9_inheritance.json**: Example curriculum content

## Learning Projects

Here are some projects you can try to enhance your learning:

### Beginner Projects

1. **Add a New Theme**: Create a new color theme for the interface
   - Modify the CSS in templates/index.html
   - Add a theme selector dropdown

2. **Add a New Curriculum Topic**: Create content for a topic you're studying
   - Follow the JSON format in existing curriculum files
   - Test how the search algorithm finds your content

3. **Improve Error Messages**: Make the error messages more helpful
   - Find where errors are handled in app.py
   - Modify the messages to be more descriptive

### Intermediate Projects

1. **Add Code Syntax Highlighting**: Enhance code examples with syntax highlighting
   - Research JavaScript libraries like Prism or Highlight.js
   - Implement the library in the templates

2. **Create a Student Dashboard**: Build a page that shows previous questions
   - Create a new route in app.py
   - Design a new HTML template
   - Query the database for conversation history

3. **Implement a Feedback System**: Allow students to rate responses
   - Add a rating UI component
   - Create a database table to store ratings
   - Add functions to record and analyze feedback

### Advanced Projects

1. **Improve the Search Algorithm**: Make the question matching more accurate
   - Study the `search_curriculum()` function
   - Research natural language processing techniques
   - Implement a more sophisticated matching algorithm

2. **Add a Code Execution Environment**: Allow students to run Java code examples
   - Research sandboxed code execution
   - Implement a secure execution environment
   - Add UI components for code input and output

3. **Create a Mobile App Version**: Build a mobile interface for the application
   - Research responsive design or native app development
   - Create mobile-friendly templates
   - Test on different device sizes

## AP Computer Science Connections

Here's how the CodeCoach AI codebase connects to AP Computer Science topics:

### AP CS A (Java) Connections

| AP CS A Topic | Where to Find It in CodeCoach AI |
|---------------|----------------------------------|
| Classes & Objects | Study how the Flask app is structured with functions and routes |
| Methods | Look at the Python functions in app.py |
| Inheritance | Study the curriculum content in unit9_inheritance.json |
| Arrays & ArrayLists | See how lists are used in the search algorithm |
| Loops & Conditionals | Find examples throughout app.py |
| Exception Handling | Look at try/except blocks in database operations |

### AP CS Principles Connections

| AP CSP Topic | Where to Find It in CodeCoach AI |
|--------------|----------------------------------|
| The Internet | See how HTTP requests/responses work in Flask |
| Data | Examine the SQLite database and JSON structures |
| Algorithms | Study the search algorithm implementation |
| Programming | Explore the Python code throughout the application |
| Impact of Computing | Consider how this tool affects education access |

## How to Ask Questions

When using CodeCoach AI for tutoring:

1. **Be Specific**: Ask clear, focused questions
2. **Mention Topics**: Include key terms from your curriculum
3. **Show Your Work**: If asking about code, include your attempt
4. **Follow Up**: Ask clarifying questions if needed

## Contributing Your Improvements

If you make improvements to CodeCoach AI, consider contributing them back:

1. **Fork the Repository**: Create your own copy on GitHub
2. **Make Your Changes**: Implement your improvements
3. **Test Thoroughly**: Make sure everything still works
4. **Submit a Pull Request**: Share your changes with the community

Your contributions can help other students across Minnesota!

## Learning Resources

To deepen your understanding of the technologies used in CodeCoach AI:

- **Python**: [Official Python Tutorial](https://docs.python.org/3/tutorial/)
- **Flask**: [Flask Documentation](https://flask.palletsprojects.com/)
- **SQLite**: [SQLite Tutorial](https://www.sqlitetutorial.net/)
- **HTML/CSS/JavaScript**: [MDN Web Docs](https://developer.mozilla.org/)
- **Git**: [Git Handbook](https://guides.github.com/introduction/git-handbook/)

---

Remember, the best way to learn programming is by doing! Don't be afraid to experiment with the code, break things, and learn from your mistakes. Happy coding!
