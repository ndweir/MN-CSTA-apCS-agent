# CodeCoach AI

## An Open Source AP Computer Science Tutoring Assistant

CodeCoach AI is an accessible, curriculum-aligned tutoring assistant designed specifically for Minnesota high school students taking Advanced Placement Computer Science courses (AP CS A and AP CS Principles). This open-source project aims to provide 24/7 support for students learning computer science concepts, with strict alignment to College Board curriculum standards.

## 🎯 Project Goals

- Provide equitable access to high-quality CS tutoring for all Minnesota students
- Support after-hours learning when teachers aren't available
- Ensure strict alignment with official AP CS curriculum standards
- Create an accessible platform that works for all students, including those with disabilities
- Offer a transparent, open-source solution that students can study, modify, and learn from

## ✨ Features

### Curriculum Alignment
- **AP CS A**: Complete coverage of Java programming concepts, classes, inheritance, and algorithms
- **AP CS Principles**: Coverage of computing concepts, algorithms, data, internet, and programming
- **College Board Approved**: Uses only official curriculum materials and standards

### Educational Design
- **Structured Responses**: Clear, organized explanations with headers and sections
- **Code Examples**: Practical Java code samples that demonstrate concepts
- **Practice Exercises**: Suggested activities to reinforce learning
- **Common Mistakes**: Guidance on errors to avoid

### Accessibility Features
- **Screen Reader Compatible**: ARIA labels and semantic HTML
- **Keyboard Navigation**: Full functionality without a mouse
- **Visual Adjustments**: Dark mode and adjustable text size
- **Clear Typography**: High-contrast, readable text

### Teacher Tools
- **Admin Dashboard**: Monitor student usage and questions
- **Curriculum Management**: Upload and organize teaching materials
- **Usage Analytics**: Track most common questions and topics
- **Data Retention Controls**: Manage student data in compliance with school policies

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ndweir/apCS-agentic-ai.git
   cd apCS-agentic-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the web interface**
   Open a web browser and navigate to `http://localhost:5001`

5. **Access the admin panel** (for teachers)
   Navigate to `http://localhost:5001/admin`

## 🧠 How It Works

### Architecture Overview

CodeCoach AI uses a Flask-based web application with the following components:

1. **Web Interface**: HTML/CSS/JavaScript frontend for student interactions
2. **Flask Backend**: Python-based server handling requests and responses
3. **Curriculum Database**: JSON-based storage of AP CS content
4. **Search Algorithm**: Natural language processing to match questions with curriculum
5. **Admin Dashboard**: Teacher interface for monitoring and management

### Directory Structure

```
codecaoch-ai/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── curriculum/            # Curriculum content
│   ├── ap_cs_a/          # AP Computer Science A materials
│   └── ap_cs_principles/  # AP Computer Science Principles materials
├── templates/             # HTML templates
│   ├── index.html         # Student interface
│   └── admin.html         # Teacher interface
└── codecoach.db           # SQLite database for conversation logs
```

### Adding Curriculum Content

Teachers can add curriculum content in JSON format through the admin interface. Each curriculum file follows this structure:

```json
{
  "title": "Unit Title",
  "description": "Unit description",
  "topics": {
    "topic_id": {
      "title": "Topic Title",
      "keywords": ["keyword1", "keyword2"],
      "content": "Detailed content with markdown formatting..."
    }
  }
}
```

## 🔒 Privacy & Security

- **Data Retention**: Conversations are stored with automatic expiration (default: 365 days)
- **IP Logging**: For teacher identification of student sessions only
- **No Personal Data**: No student accounts or personal information required
- **Automatic Purging**: Expired data is automatically removed
- **Access Controls**: Admin interface restricted to teachers

## 🧪 For Students: Learning From The Code

This project isn't just a tool to use - it's also a learning opportunity! Here are some ways students can learn from this codebase:

### Python Web Development
- Study how Flask routes work in `app.py`
- Learn about HTML templates and Jinja2 in the `templates/` directory
- Understand HTTP requests and responses in the chat functionality

### Database Management
- Examine the SQLite database implementation
- Learn about data models and schema design
- Study the data retention and privacy mechanisms

### Search Algorithms
- Review the question-matching algorithm in `search_curriculum()` function
- Learn about keyword extraction and topic matching
- Understand how to improve search results with scoring mechanisms

### Accessibility
- Study the WCAG-compliant HTML structure
- Learn about screen reader compatibility
- Understand how dark mode and text sizing are implemented

## 🤝 Contributing

We welcome contributions from students, teachers, and developers! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add some amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Ideas for Student Contributions
- Add new curriculum content
- Improve the search algorithm
- Enhance accessibility features
- Create new UI themes
- Add support for additional programming languages

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- College Board for AP Computer Science curriculum materials
- Minnesota high school CS teachers for curriculum guidance
- Flask and Bootstrap teams for the web framework and UI components

## 📞 Contact

For questions or feedback, please open an issue on this repository or contact the project maintainer.
