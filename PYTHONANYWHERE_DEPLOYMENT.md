# Deploying CodeCoach AI on PythonAnywhere (Free Tier)

This guide will walk you through deploying the CodeCoach AI application on PythonAnywhere's free tier, which is the most cost-effective hosting option.

## Prerequisites

- A PythonAnywhere account (sign up at [pythonanywhere.com](https://www.pythonanywhere.com))
- Your GitHub repository with the CodeCoach AI code

## Step 1: Sign Up for PythonAnywhere

1. Go to [pythonanywhere.com](https://www.pythonanywhere.com)
2. Sign up for a free account (no credit card required)

## Step 2: Set Up a Web App

1. After logging in, click on the **Web** tab
2. Click **Add a new web app**
3. Click **Next**
4. Select **Flask** as your framework
5. Select **Python 3.8** (or the latest available version)
6. Set your project path to `/home/yourusername/codecoach-ai`
7. For the WSGI configuration file, use the default path

## Step 3: Clone Your Repository

1. Click on the **Consoles** tab
2. Start a new **Bash console**
3. Clone your repository:
   ```bash
   git clone https://github.com/ndweir/MN-CSTA-apCS-agent.git codecoach-ai
   cd codecoach-ai
   ```

## Step 4: Set Up a Virtual Environment

1. In the Bash console, create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Step 5: Configure the WSGI File

1. Go to the **Web** tab
2. Click on the **WSGI configuration file** link
3. Replace the contents with the following:
   ```python
   import sys
   
   # Add your project directory to the Python path
   path = '/home/yourusername/codecoach-ai'
   if path not in sys.path:
       sys.path.append(path)
   
   # Import your Flask application
   from wsgi import application
   ```
4. Save the file

## Step 6: Configure Static Files (Optional)

1. Go to the **Web** tab
2. Under **Static files**, add the following mapping:
   - URL: `/static/`
   - Directory: `/home/yourusername/codecoach-ai/static/`

## Step 7: Update the Virtual Environment Path

1. Go to the **Web** tab
2. Under **Virtualenv**, enter the path to your virtual environment:
   ```
   /home/yourusername/codecoach-ai/venv
   ```

## Step 8: Reload Your Web App

1. Go to the **Web** tab
2. Click the **Reload** button for your web app

## Step 9: Access Your Application

Your application will now be available at:
```
yourusername.pythonanywhere.com
```

## Troubleshooting

If your application doesn't work:

1. Check the **Web** tab for error messages
2. Look at the error log files
3. Make sure all required packages are installed
4. Ensure the database file is writable

## Maintaining Your Application

### Updating Your Application

When you make changes to your GitHub repository:

1. Open a Bash console
2. Navigate to your project directory:
   ```bash
   cd codecoach-ai
   ```
3. Pull the latest changes:
   ```bash
   git pull
   ```
4. Reload your web app from the **Web** tab

### Free Tier Limitations

The free tier of PythonAnywhere has some limitations:

- Your app may sleep after periods of inactivity
- Limited CPU time and bandwidth
- Limited storage (512MB)
- No custom domains (you'll use yourusername.pythonanywhere.com)

These limitations are acceptable for a classroom demonstration or low-traffic educational tool.

## Cost Comparison

| Hosting Option | Monthly Cost | Features |
|----------------|--------------|----------|
| PythonAnywhere (Free) | $0 | 512MB storage, limited CPU |
| PythonAnywhere (Hacker) | $5 | 2GB storage, more CPU, custom domain |
| Render.com (Free) | $0 | Auto-sleep after inactivity |
| Railway.app | $5+ | 1GB RAM, 1 vCPU |
| Heroku (Eco) | $5 | 1x dyno, sleeps after 30 min inactivity |

PythonAnywhere's free tier is the most cost-effective option for hosting CodeCoach AI.
