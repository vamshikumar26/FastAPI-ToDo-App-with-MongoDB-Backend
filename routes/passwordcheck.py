import re
#checking password is correct or not
def checkpassword(password):
    
    pattern = re.compile( r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$")
    
    return bool(pattern.match(password))
    
    