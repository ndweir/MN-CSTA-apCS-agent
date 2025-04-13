# Setting Up Admin Credentials on PythonAnywhere Free Tier

Since PythonAnywhere's free tier doesn't have a dedicated environment variables section in the web interface, we've implemented a special solution using a `secrets.py` file.

## Steps to Set Up Admin Credentials

1. **SSH into your PythonAnywhere account** using the Bash console

2. **Navigate to your project directory**:
   ```bash
   cd mysite
   ```

3. **Create a secrets.py file** (this file will NOT be in Git):
   ```bash
   nano secrets.py
   ```

4. **Add your credentials** to the file:
   ```python
   # Environment variables for CodeCoach AI
   SECRET_KEY = 'your_secure_random_key_here'
   ADMIN_USERNAME = 'your_admin_username'
   ADMIN_PASSWORD = 'your_admin_password'
   ```

5. **Save the file** by pressing `Ctrl+O`, then `Enter`, then `Ctrl+X` to exit

6. **Set proper permissions** to restrict access:
   ```bash
   chmod 600 secrets.py
   ```

7. **Reload your web app** from the Web tab

## How It Works

The application has been modified to check for credentials in this order:

1. Environment variables (if available)
2. The secrets.py file (if it exists)
3. Default fallback values (only for development)

This approach keeps your credentials secure while working with the limitations of the free tier.

## Important Security Notes

1. **Never commit secrets.py to Git** (it's already in .gitignore)
2. **Use strong, unique passwords** for your admin credentials
3. **Change your credentials periodically** for better security
4. **The secrets.py file is only visible to your PythonAnywhere account**

## Accessing the Admin Interface

After setting up your credentials:

1. Navigate to `MNcodecoach.pythonanywhere.com/admin`
2. You'll be redirected to the login page
3. Enter the username and password you set in secrets.py
4. After successful authentication, you'll have access to the admin panel
