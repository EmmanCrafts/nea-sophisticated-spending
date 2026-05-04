# Simple Flask Login App


---

## 🚀 Getting Started

Follow these steps to download and run the application on your computer.

### Step 1: Download the Code from GitHub

1. Go to the GitHub repository page
2. Click the green **"Code"** button
3. Click **"Download ZIP"**
4. Once downloaded, find the ZIP file in your Downloads folder
5. **Right-click** the ZIP file and select **"Extract All..."** (Windows) or double-click to unzip (Mac)
6. Open the extracted folder - you should see files like `main.py`, `models.py`, etc.

### Step 2: Open Terminal/Command Prompt

**Mac:**
- Press `Cmd + Space`, type `Terminal`, and press Enter



### Step 3: Navigate to the Project Folder

Use the `cd` command to navigate to where you extracted the files:


**Tip:** You can type `cd ` (with a space) and then drag the folder into the terminal to auto-fill the path!

### Step 4: Create a Virtual Environment

A virtual environment keeps your project's packages separate from other Python projects.

```bash
python -m venv venv
```

If that doesn't work, try:
```bash
python3 -m venv venv
```

You should now see a new folder called `venv` in your project directory.

### Step 5: Activate the Virtual Environment


**Mac/Linux:**
```bash
source venv/bin/activate
```

✅ **How to know it worked:** You should see `(venv)` at the beginning of your terminal line. 


### Step 6: Install the Required Packages

```bash
pip install -r requirements.txt
```

This installs Flask and other packages needed to run the app.

### Step 7: Run the Application

```bash
python main.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### Step 8: Open in Your Browser

Open your web browser and go to:

👉 **http://127.0.0.1:5000**

You should see the login page! 🎉

### Step 9: Test the App

1. Click **"Register"** to create an account
2. Fill in a username, email, and password
3. After registering, log in with your credentials
4. You should see the Dashboard!

### Stopping the Server

To stop the server, go back to your terminal and press `Ctrl + C`.

### Restarting Later

Every time you want to work on your project:
1. Open terminal
2. Navigate to your project folder (`cd path/to/flask_app`)
3. Activate the virtual environment (Step 5)
4. Run the server (`python main.py`)

---

## 📁 Project Structure

```
flask_app/
├── main.py              # All routes/views
├── models.py            # Database models
├── requirements.txt     # Python dependencies
└── templates/           # HTML templates
    ├── base.html        # Base template with Bootstrap
    ├── index.html       # Login page
    ├── register.html    # Registration page
    ├── forgot_password.html
    └── dashboard.html   # User dashboard
```

---

## 🔍 How the App Works

| Route | Description |
|-------|-------------|
| `/` | Home page with login form |
| `/login` | Handles login form submission |
| `/register` | Registration page and form handling |
| `/forgot-password` | Forgot password page |
| `/dashboard` | Protected page (must be logged in) |
| `/logout` | Logs out user and redirects to home |

---

## 📝 NEXT STEPS: Your Assignment

Now that you have the app running, your task is to extend it with the following requirements:

### Task 1: Design the Dashboard

The current dashboard (`templates/dashboard.html`) is very basic. Your job is to design it using **Bootstrap** components play with Boostrap components to make this page look like the design you have in documentation.

Feel free to design other pages, follow what I have done in index.html and other files


---

### Task 2: Add Other Models

The application currently only has a `User` model. Add at least **other models** to `models.py`, you can start by copy pasting the `User` model and Rename the class and then rename the field variables as necessary.


---

Good luck  🚀
