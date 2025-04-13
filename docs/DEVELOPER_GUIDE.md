# CodeCoach AI Developer Guide

This guide is designed to help students and developers understand how CodeCoach AI works and how to contribute to the project. Whether you're looking to learn from the codebase or add new features, this document will help you get started.

## Table of Contents

1. [Application Architecture](#application-architecture)
2. [Core Components](#core-components)
3. [Search Algorithm](#search-algorithm)
4. [Database Schema](#database-schema)
5. [Adding New Curriculum Content](#adding-new-curriculum-content)
6. [Accessibility Features](#accessibility-features)
7. [Security Considerations](#security-considerations)
8. [Testing](#testing)

## Application Architecture

CodeCoach AI follows a simple but effective architecture:

```
[Browser] <--> [Flask Web Server] <--> [Curriculum Files] + [SQLite Database]
```

- **Frontend**: HTML/CSS/JavaScript with Bootstrap for responsive design
- **Backend**: Python Flask application
- **Data Storage**: 
  - JSON files for curriculum content
  - SQLite database for conversation logs and access tracking

## Core Components

### 1. Flask Application (`app.py`)

The main application file contains several key components:

- **Route Handlers**: Process HTTP requests and render templates
- **Search Functions**: Match student questions to curriculum content
- **Database Operations**: Log conversations and track access
- **Admin Functions**: Manage curriculum and view analytics

### 2. Templates

- **index.html**: The main student interface with chat functionality
- **admin.html**: Teacher dashboard for monitoring and management

### 3. Curriculum Files

JSON-structured content organized by AP CS units:

```
curriculum/
├── ap_cs_a/
│   ├── unit1_primitive_types.json
│   ├── unit9_inheritance.json
│   └── ...
└── ap_cs_principles/
    ├── unit1_digital_information.json
    └── ...
```

## Search Algorithm

The heart of CodeCoach AI is the `search_curriculum()` function, which matches student questions to the appropriate curriculum content. Here's how it works:

1. **Text Preprocessing**:
   - Convert question to lowercase
   - Remove punctuation and special characters
   - Extract keywords

2. **Matching Process**:
   - Check for direct matches with topic titles
   - Look for keyword overlap with curriculum content
   - Calculate a relevance score for each potential match

3. **Response Generation**:
   - Return the highest-scoring content
   - Include source information for transparency
   - Format response for readability

### Key Code Snippet:

```python
def search_curriculum(question):
    # Convert question to lowercase for case-insensitive matching
    question_lower = question.lower()
    
    # Check for general learning requests
    if any(phrase in question_lower for phrase in ["teach me", "learn about", "explain", "what is", "what's"]):
        # Handle general learning requests
        # ...
    
    # Calculate scores for each topic based on keyword matches
    # ...
    
    return best_match, source
```

## Database Schema

CodeCoach AI uses SQLite for data storage with the following tables:

### `conversations` Table
- `id`: Unique identifier
- `session_id`: Browser session identifier
- `ip_address`: User's IP address (for teacher identification)
- `timestamp`: When the conversation occurred
- `question`: Student's question
- `answer`: System's response
- `source`: Curriculum source used
- `retention_date`: When this record should be deleted

### `access_log` Table
- `id`: Unique identifier
- `ip_address`: User's IP address
- `timestamp`: When the access occurred
- `action`: What the user did (e.g., "student_access", "admin_access")

### `data_retention_policy` Table
- `id`: Unique identifier
- `entity_type`: Type of data (e.g., "conversations")
- `retention_days`: How many days to keep the data
- `description`: Human-readable explanation

## Adding New Curriculum Content

To add new curriculum content:

1. **Create a JSON File**: Follow the structure below
2. **Place in Curriculum Directory**: Add to the appropriate AP CS folder
3. **Update Admin Interface**: Add the new file to the curriculum list

### JSON Structure:

```json
{
  "title": "Unit Title",
  "description": "Brief description of this unit",
  "topics": {
    "topic_id_1": {
      "title": "Topic Title",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "content": "Detailed explanation with **markdown** formatting..."
    },
    "topic_id_2": {
      "title": "Another Topic",
      "keywords": ["keyword4", "keyword5"],
      "content": "More detailed content..."
    }
  }
}
```

## Accessibility Features

CodeCoach AI is designed to be accessible to all students:

1. **Semantic HTML**: Proper heading structure and ARIA attributes
2. **Keyboard Navigation**: All functions accessible without a mouse
3. **Screen Reader Support**: Alt text and descriptive labels
4. **Visual Adjustments**: 
   - Dark mode toggle
   - Text size controls
   - High contrast options

## Security Considerations

When working with the codebase, keep these security principles in mind:

1. **Data Minimization**: Only collect what's necessary
2. **Automatic Purging**: Implement data retention policies
3. **Input Validation**: Sanitize all user inputs
4. **Access Controls**: Restrict admin functions appropriately

## Testing

To test CodeCoach AI:

1. **Manual Testing**:
   - Try various question formats
   - Test accessibility features
   - Verify admin functions

2. **Automated Testing** (future enhancement):
   - Unit tests for search functions
   - Integration tests for database operations
   - End-to-end tests for user flows

## Contributing

We encourage students to contribute to CodeCoach AI! Some ideas:

- Add new curriculum units
- Improve the search algorithm
- Enhance the UI/UX
- Add new features for teachers or students

Follow the contribution guidelines in the main README.md file.

---

This guide is a living document. If you have suggestions for improvements, please submit a pull request!
