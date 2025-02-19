# Image-Steganography-AES
AES-powered image steganography using Python and Gradio.

This project implements AES-encrypted image steganography to securely hide messages inside images.     
It combines cryptography for encryption and image manipulation to embed and retrieve hidden messages.

## 1. How Does the Code Work?
The code has two main parts:

## Encryption Process (Hiding the Message)

### Input:
-An image (e.g., .png, .jpg, etc.)  
-A secret message  
-A password to encrypt the message  

### AES-256 Encryption:
-The message is encrypted using AES (Advanced Encryption Standard) with a 256-bit key.  
-A salt and IV (Initialization Vector) are generated to enhance security.  
-The encrypted message is encoded using Base64 for easy storage.  

### Image Steganography:  
-The length of the encrypted message is stored in the first pixel.  
-The encrypted message is then embedded into the green channel of the image pixels.  

### Output:
The program saves the modified image as encrypted_image.png with the hidden message.  

## Decryption Process (Revealing the Message)  

### Input:
-An encrypted image (with the hidden message)  
-The correct password  

### Extracting the Message:
-The code reads the message length from the first pixel.  
-It then retrieves the encrypted message from the green channel of the image.  

### AES Decryption:
-The encrypted message is decoded using the AES key derived from the password.  
-If the password is correct, the original message is revealed.  

### Output:
-If the password is correct, it prints the decrypted message.  
-If the password is wrong, it returns "Decryption Failed! Incorrect Password.    

## 2. Key Concepts
### AES-256 Encryption: Industry-standard encryption algorithm for securing data.  
-PBKDF2 Key Derivation: Converts passwords into a cryptographic key using SHA-256 and 100,000 iterations for better security. 

### Steganography: Hides information inside images without changing their visible appearance.  
-Google Colab & Gradio: Allows running and interacting with the application via a user-friendly interface.  

## 3. Code Flow
-Encryption  
-Encrypt the message with AES.  
-Embed the encrypted message into the image.  
-Save the modified image.  
-Decryption  
-Extract the encrypted message from the image.  
-Decrypt using the password.  
-Reveal the original message if the password is correct.  

## 4. Why Use AES Encryption?
-Secure: AES-256 is considered unbreakable with modern computing power.  
-Privacy: Even if the image is intercepted, the message remains encrypted.  
-Stealthy: The image looks the same to the naked eye but holds hidden information.  
