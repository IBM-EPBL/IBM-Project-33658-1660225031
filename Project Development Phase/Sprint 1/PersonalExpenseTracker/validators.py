from .models import User
class UserValidator:
    def validate(self,firstName,lastName,userName,email,password):
        firstNameMsg = self.noneFieldValidator(firstName,"First Name")
        lastNameMsg = self.noneFieldValidator(lastName,"Last Name")
        userNameMsg = self.uniqueAndNoneFieldUsernameValidator(userName)
        emailMsg = self.uniqueAndNoneFieldEmailValidator(email)
        passwordMsg = self.noneFieldValidator(password,"Password")
        if self.checkInstance(firstNameMsg,str):
            return firstNameMsg
        elif self.checkInstance(lastNameMsg,str):
            return lastNameMsg
        elif self.checkInstance(userNameMsg,str):
            return userNameMsg
        elif self.checkInstance(emailMsg,str):
            return emailMsg
        elif self.checkInstance(passwordMsg,str):
            return passwordMsg
        else:
            return True
    def checkInstance(self,type,validator):
        return isinstance(type,validator)
    def uniqueAndNoneFieldUsernameValidator(self,data):
        if data=="":
            return "* {0} required field".format("Username")
        else:
            user_data = User.query.filter_by(userName=data).all()
            print(type(user_data),user_data)
            if user_data:
                return "Username already exists please choose another one"
        return True
    def uniqueAndNoneFieldEmailValidator(self,data):
        if data=="":
            return "* {0} required field".format("Email")
        else:
            email_data = User.query.filter_by(email=data).all()
            if email_data:
                return "Email already exists please choose another one"
            return True
    def noneFieldValidator(self,data,field):
        if data=="":
            return "* {0} required field".format(field)
        return True