from passlib.context import CryptContext

# Initialize the CryptContext for bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Test password to hash
plain_password = "managerpassword123"

# Hash the password
hashed_password = pwd_context.hash(plain_password)


# Verify the hashed password against the original one
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Output results for debugging
print(f"Plain Password: {plain_password}")
print(f"Hashed Password: {hashed_password}")

# Check if the password matches
if verify_password(plain_password, hashed_password):
    print("Password verification successful!")
else:
    print("Password verification failed.")
