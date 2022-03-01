# PasswordVault

### Background
This app was created as my portfolio project for CS 361 at OSU.

This app allows a user to create a master password which they can use to access their stored
passwords for other accounts. Once the user creates a master account, they can log in to the
app and create, edit, or delete their passwords.

The main functionality of this app is listed below:
- Allows user to create, read, update, and delete passwords for their accounts
- Provides user with a way to copy the password to the clipboard for 15 seconds
- Incorporates a random password generator so users don't have to create their own passwords
- Provides user with a strength rating of their passwords using the information bit entropy calculation

This app was heavily inspired by the KeePass software I currently use at work.

### How to Install
1. Ensure that you have MySQL server installed
2. Run the "database_definitions.sql" script from the MySQL root account, or a similar
account that has CREATE privileges.
3. Install the project dependencies using the below terminal command
    ~~~
    pip install -r requirements.txt
    ~~~
4. You are now ready to use to app. Simply create a master account and log in to begin.

### Using the App
Below screenshots show a basic overview of the functionality  
  
Login Screen  
![Login Screen](/screenshots/login_screen.png)  
Main Screen  
![Main Screen](/screenshots/main_screen.png)  
Add a weak password  
![Add a weak password](/screenshots/add_weak_password.png)  
Add a strong password  
![Add a strong password](/screenshots/add_strong_password.png)  
Copy a stored password  
![Copy password](/screenshots/copy_password.png)  
Edit an existing passwrod  
![Edit existing password](/screenshots/edit_password.png)  

### Discussion: Password Bit Entropy
The password strength function in this application uses a calculation known
as information entropy, which is measured in bits. A random password's information 
entropy can be calculated using the formula  **H = log<sub>2</sub>N<sup>L</sup>** 
where H is the number of bits, N is the number of possible symbols per character, 
and L is the password length.
  
In this calculation, N<sup>L</sup> calculates the number of unique passwords of 
length L that could be generated using N symbols. Taking the log base 2 of this
value provides us with the number of bits needed to represent N<sup>L</sup>. The resulting 
bit value is useful because an increase of 1 bit entropy means that the number of possible 
unique passwords has doubled, meaning it would take twice as long for a brute force attack 
to guess the password. The bit entropy value is also much smaller, and, thus, more
readable than the values of N<sup>L</sup>. So, the bit entropy provides a better way for 
us to compare the strength of passwords compared to looking at just N<sup>L</sup> alone. 

The actual strength of a password, as determined by its bit entropy value, is somewhat
subjective, but there are guidelines that have been published discussing this in detail.
For example, a password with less than 28 bits of entropy is very weak. A password with
128 bits or more is considered very strong. See the second link below for more detailed
information on this topic.

Sources used for above information:
- https://en.wikipedia.org/wiki/Password_strength#Required_bits_of_entropy
- https://iocane.com.au/talking-passwords-and-entropy/


### Password Generator Microservice
The password generator functionality for this app is achieved using my teammate's
microservice. For the password generator to work, the RPyC server must be running
on localhost.  
Microservice code can be found here: https://github.com/colinjoss/random-string_microservice  
Author of microservice: @colinjoss

