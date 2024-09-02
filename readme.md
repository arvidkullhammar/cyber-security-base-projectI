# Cyber Security Base Project

This is my project for the Cyber Security Base course at the University of Helsinki.

It is a web application with different security flaws. I point out the flaws in the essay below and refer to comments in the code.

## Running the Project

To run the project, you need Django and Python installed. If you use a virtual environment, you can install the dependencies using the `requirements.txt` file.

1. **Clone the Repository**: Clone the repository to your local machine.

   ```sh
   git clone https://github.com/arvidkullhammar/cyber-security-base-projectI.git
   ```

2. **Navigate to the Project Directory**: Change directory into the project directory.

   ```sh
   cd cyber-security-base-projectI
   ```

3. **Install Dependencies**: If you're using a virtual environment, activate it and install the dependencies using the `requirements.txt` file.

   ```sh
   # Activate virtual environment (optional)
   source myenv/bin/activate  # On macOS/Linux
   myenv\Scripts\activate.bat  # On Windows

   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Run the Server**: Start the Django development server.

   ```sh
   python manage.py runserver
   ```

5. **Access the Application**: Open a web browser and navigate to `http://localhost:8000/`.

## Security Flaws

I have identified several security flaws in the application. These flaws are documented in the essay below and referenced in the code comments.
FLAW 1:
exact source link: https://github.com/arvidkullhammar/cyber-security-base-projectI/blob/d7958194416e60698f6d83bd6a72d99eae03ebac/app/views.py#L21

Description: 
This flaw is related to Broken Access Control. Access control ensures that users can only access resources they are authorized to.
In this case, the page that lists the user’s notes is accessible by anyone, even if they are not logged in.
Specifically, the notes view does not do any access control check. This means anyone visiting the web page can view the notes of any given user as long as they know the URL to view them (/notes/:name).

How to fix it: To address this issue, we should ensure that only an authenticated user can visit the notes page. Django has a built-in decorator to add to a view (@login_required).
Adding this will redirect the user to the login page if they are not logged in.
Also, users should only be able to access their own notes. We can implement this by verifying that the logged-in user ID matches the ID of the requested user. 
If the user id’s does not match, the server returns a 403 forbidden response.



FLAW 2:
exact source link: https://github.com/arvidkullhammar/cyber-security-base-projectI/blob/d7958194416e60698f6d83bd6a72d99eae03ebac/projectI/settings.py#L25C36-L25C37

Description: This flaw is related to Security Misconfiguration. Common flaws related to this topic are security functionality not enabled, improperly configured permissions, and in this case, application error handling exposing sensitive information. 
Django has a debug mode that makes it easier for developers to track errors in their applications. It exposes the stack trace and environment information when opening a faulty URL. If debug mode is not turned off in production, malicious users can utilize this information to exploit weaknesses they find in the code.

How to fix it: Debug mode is set to True by default when creating a new Django project. Before deploying the application it needs to be turned off. This is done by going into the settings.py file and setting debug to False.


FLAW 3:
exact source link: https://github.com/arvidkullhammar/cyber-security-base-projectI/blob/d7958194416e60698f6d83bd6a72d99eae03ebac/app/views.py#L33
 
Description: This flaw is related to Security Logging and Monitoring failures. It is important to detect and register any unauthorized attempts to access data on your web application. Most web hosting platforms enable you to save the server terminal to logs, so you can review what is happening. Django already prints out all requests that come in along with the response code, but it could be more specific. For example, when an account tries to access another user's notes we should register what account is doing the request. This is valuable information as it is a good way to detect if an account is performing suspicious activity.

How to fix it: If the fix for flaw 2 is implemented, add a print statement with additional information about the request in the code block that handles unauthorized attempts.

FLAW 4:
exact source link: https://github.com/arvidkullhammar/cyber-security-base-projectI/blob/d7958194416e60698f6d83bd6a72d99eae03ebac/app/views.py#L68
 
Description: This flaw is related to Injection. It introduces the risk of users sending malicious data that can perform database commands that should not be possible. The specific flaw in this web application is that when a user deletes a note, it sends a GET request with the note ID as a path variable. That path variable is then directly inserted into a raw SQL query. The query is only supposed to delete the note related to the ID, but with this flaw, more data can be added to the query. 
For example, if you send this request: /delete?note_id=1%20OR%201=1 the SQL query will be "DELETE FROM app_note WHERE id = {note_id} OR 1=1”. 
This would delete every note in the database since the second condition is always true.

How to fix it: Django offers a built-in ORM to do database queries. It prevents unsanitized data from being added to the database operation. 



FLAW 5:
exact source links:  https://github.com/arvidkullhammar/cyber-security-base-projectI/blob/d7958194416e60698f6d83bd6a72d99eae03ebac/app/views.py#L59

https://github.com/arvidkullhammar/cyber-security-base-projectI/blob/d7958194416e60698f6d83bd6a72d99eae03ebac/app/templates/pages/notes.html#L16

 
Description: This flaw is related to CSRF. It introduces the risk of attackers using a malicious website to make unintended requests to the web application. CSRF tokens are a protection against these types of attacks, where a token is created on authentication and then required on each subsequent request. Django has an out-of-the-box CSRF protection middleware that stores a CSRF token as a cookie when a user authenticates and it is then including the token with each request. However, GET requests are not protected by CSRF by default. Since the request to delete notes is a GET request a hacker could have the victim visit a website that makes an unintended request to this endpoint.

How to fix it: To fix this issue, we change the HTTP method used with this view to a POST request. Not only would this enable the CSRF protection by default, but it would also align with best practices regarding HTTP requests in general. We also update the form in the notes template by adding the csrf token to the form and changing the method to a POST request.


I used Grammarly to spellcheck the essay
...
