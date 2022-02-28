# PasswordVault

Portfolio Project for CS 361

### Background
Inspired by the KeePass software I currently use at work.

### How to Install

### Using the App
Screenshots

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
to guess the password. Thus, the bit entropy provides a better way for us to compare the
strength of passwords compared to just N<sup>L</sup> alone.

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

