# Cryptography Comparative Analysis Tool
## Overview
This project is a Cryptography Comparative Analysis Tool designed for easily encrypting and decrypting the contents of files using two algorithms (AES and RSA) and three frameworks/libraries (OpenSSL, PyCryptography, and PyCryptodome). The primary aim of this tool is to provide a statistical comparison of encryption/decryption performance across different algorithms and frameworks.

## Features
- **Encryption and Decryption**: Supports encryption and decryption of files using AES and RSA algorithms.
- **Multiple Framework Support**: Utilizes OpenSSL, PyCryptography, and PyCryptodome for encryption and decryption operations.
- **Performance Measurement**: Measures the time taken for encryption and decryption operations and stores performance metrics in a SQLite database.
- **Key Generation**: Provides a key generation service based on the chosen algorithm.
- **Business Persistence Presentation (BPP) Architecture**: Follows the BPP architectural model for separation of concerns and modularity.
- **Graphical User Interface (GUI)**: Built with PySide2 for an intuitive user interface.

## Development Details
- **Logging**: Implemented logging to record application events and errors, facilitating debugging and troubleshooting.
- **Exception Handling**: Utilized try-except blocks for robust error handling, ensuring graceful degradation in case of unexpected errors.
- **Modularization**: Modularized the codebase into separate modules and classes to promote code organization and maintainability.
- **Design Principles**: Designed with flexibility and reusability in mind, utilizing abstract classes and interface-like classes in Python to easily add more algorithms and frameworks.
- **Code Comments**: Provided detailed comments throughout the codebase to enhance readability and understanding for developers.


## Cryptographic Algorithms
### AES (Advanced Encryption Standard)
AES is a symmetric encryption algorithm widely used for securing sensitive data. It supports key lengths of 128, 192, or 256 bits, making it suitable for various security requirements. AES operates on fixed-size blocks of data and is considered secure for practical use.

### RSA (Rivest-Shamir-Adleman)
RSA is an asymmetric encryption algorithm commonly used for secure data transmission. It relies on the difficulty of factoring large prime numbers to ensure security. RSA involves the generation of public and private key pairs, where the public key is used for encryption and the private key is used for decryption.

## Frameworks/Libraries
### OpenSSL
OpenSSL is a robust open-source toolkit implementing the SSL and TLS protocols. It provides cryptographic functions for secure communication over networks. OpenSSL supports various cryptographic algorithms and is widely used in applications requiring secure data transmission.

### PyCryptography
PyCryptography is a Python library providing cryptographic primitives and recipes. It offers a high-level interface for common cryptographic operations such as encryption, decryption, signing, and verification. PyCryptography is built on top of OpenSSL and provides a Pythonic way to perform cryptographic tasks.

### PyCryptodome
PyCryptodome is a fork of the PyCrypto library and is designed to provide cryptographic primitives in Python. It offers a comprehensive range of cryptographic algorithms and protocols, including AES, RSA, HMAC, and more. PyCryptodome aims to be a reliable and efficient solution for cryptographic operations in Python.


## Database Schema
The project uses a SQLite database with the following schema:

- **File**: Stores information about files including file name, path, size, hash, and associated algorithm.
- **Key**: Contains details about encryption keys including name, value, and type (public/private).
- **Algorithm**: Defines algorithms used for encryption/decryption along with their type (symmetric/asymmetric).
- **PerformanceMetrics**: Records performance metrics such as timestamp, time taken, operation type (encryption/decryption), file ID, algorithm ID, and framework ID.
- **Framework**: Stores information about frameworks/libraries used for encryption/decryption.
- **KeyPairs**: Associates encryption keys with algorithms.
