# How to Run the Project


Download the project code from its online location.

create a virtual environment with python -m venv environmentname  and activate it per your OS

Change directory or (cd into the project) go to the project folder.

Install the tools: Run pip install -r requirements.txt command to install all the necessary libraries.

Set up the project to use your database (like PostgreSQL).

Run python manage.py makemigrations and python manage.py migrate to prepare the database for the project.

Make a superuser account with full access python manage.py createsuper

Run python manage.py runserver to start the project's server.

Now your project should be running!

# How to Log In (Authentication)

You need a special key (called a JWT token) to access the secure parts of the API.

Send your username and password to the url /api/token/.

For every secure request, you must put the key in the "Authorization" part of your request. This tells the API who you are.

If your key expires in (2hours per the project setting, you can adjust), you can use a "refresh" key to get a new one without logging in again.

#API Endpoints: What They Do
Here's a simple guide to what each API address does.

## Task

/tasks/: Get a list of tasks. Admins see all tasks, while users only see the tasks assigned to them.

/tasks/: Create a new task. Only an Admin can do this.

/tasks/<id>/: Get details for one task. Both Admins and Users can do this.

/tasks/<id>/: Change a task. Admins can change anything, but users can only change the status.

/tasks/<id>/: Delete a task. Only an Admin can do this.

# Comments
/comments/: Get a list of comments. Admins see all comments, while users see comments only on their tasks.

/comments/: Add a new comment. The system automatically knows who you are. Both Admins and Users can do this.

/comments/<id>/: Get details for one comment. Both Admins and Users can do this.

/comments/<id>/: Delete a comment. Only an Admin can do this.

# Users
/users/: Get a list of all users. Only an Admin can do this.

/users/: Create a new user account. Everyone can do this.

/users/<id>/: Delete a user. This is a "soft delete," which means the user is not permanently removed. Only an Admin can do this.

# What is "Soft Delete"?
When you "delete" a user or a task, the logic don't actually remove it from the database forever. Instead, it just mark it as "inactive." This is like moving a file to the recycling bin instead of shredding it. It keeps the data safe in case you need it later.
