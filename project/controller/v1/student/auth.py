from fastapi import APIRouter
from fastapi.responses import JSONResponse
from project.model.models import *
from datetime import datetime
from project.config.error_messages import *
import os
from project.utils.auth_utils import *
from project.component.token import *




router=APIRouter(prefix='/api/v1/student/auth')
logger = set_up_logging()


''' create acccount '''

@router.post("/create")
def create_account(json_data: ValidateAccount):
    try:
        logger.info("Create Account")
        email = json_data.email
        fname = json_data.fname
        lname = json_data.lname
        mobile = json_data.mobile
        password = json_data.password
        print(password)
        db_student = session.query(Student).filter(
            Student.email == email).first()  # check if email exists for admin
        if not db_student:
            salt = os.urandom(8)
            cf = AESCipher(salt, password)
            encrypted_value = cf.encrypt(str(password))  # encrypt the password
            
            new_student = Student(
                email = email,
                fname = fname,
                lname = lname,
                mobile = mobile,
                encrypted_password = encrypted_value,  
                salt = salt                
            )
            logger.info(f"Created student: {email}")
            session.add(new_student)
            session.commit()

            res_status = True
            res_message = SUCC_DEFAULT
            logger.info(res_message)
            status_code = 200

            return JSONResponse({
                'status': res_status,
                'status_code': status_code,
            }, status_code=status_code)


        else:
            res_status = False
            res_message = ERR_STUDENT_ALREADY_EXISTS
            logger.error(res_message)
            status_code = 400
            return JSONResponse({
                'status': res_status,
                'message': res_message,
                'status_code': status_code,
            }, status_code=status_code)


    except Exception as e:
        session.rollback()
        res_status = False
        res_message = ERR_SOMETHING_WENT_WRONG + str(e)
        logger.error(res_message)
        status_code = 500
        return JSONResponse({
            'status': res_status,
            'message': res_message,
            'status_code': status_code,
        }, status_code=status_code)


''' login '''
@router.post("/login")
def Student_Login(json_data:StudentLogin):
    try:
        logger.info("Student Login - API")

        email = json_data.email
        password = json_data.password

        data = {}

        db_student = session.query(Student).filter(Student.email == email).first()  # check if email exists

        if db_student:
            if db_student.active == True:

                salt = db_student.salt
                cf = AESCipher(salt, password)
                decrypted_value = cf.decrypt(db_student.encrypted_password)  # decrypt the password in the db
                logger.info(f"Decrypted Value : {decrypted_value}")
                print(f"Decrypted : {decrypted_value}")
                print(f"User gave : {password}")

                if decrypted_value == password:
                    print(db_student.id)
                    access_token = admin_create_access_token(int(db_student.id))
                    data['token'] = access_token #Create Access Token

                    email = db_student.email                    
                    
                    res_status = True
                    res_message = SUCC_DEFAULT
                    logger.info(res_message)
                    status_code = 200
                    return JSONResponse({
                        'status': res_status,
                        'message': res_message,
                        'status_code': status_code,
                        'data': data
                    }, status_code=status_code)

                else:
                    res_status = False
                    res_message = "Invalid password"
                    logger.error(res_message)
                    status_code = 400
                    return JSONResponse({
                        'status': res_status,
                        'message': res_message,
                        'status_code': status_code,
                    }, status_code=status_code)

            else:
                res_status = False
                res_message = "Student is inactive"
                logger.error(res_message)
                status_code = 401
                return JSONResponse({
                    'status': res_status,
                    'message': res_message,
                    'status_code': status_code,
                }, status_code=status_code)

        else:
            res_status = False
            res_message = 'Invalid student'
            logger.error(res_message)
            status_code = 400
            return JSONResponse({
                'status': res_status,
                'message': res_message,
                'status_code': status_code,
            }, status_code=status_code)

    except Exception as e:
        session.rollback()
        res_status = False
        res_message = ERR_SOMETHING_WENT_WRONG
        logger.error(res_message + " :: " + str(e))
        status_code = 500
        return JSONResponse({
            'status': res_status,
            'message': res_message,
            'status_code': status_code,
        }, status_code=status_code)
    

''' forgot password '''
@router.post('/forgot-password')
def Forgot_Password(json_data: ValidateForgotPassword):
    try:
        logger.info("Forgot Password - API :: " + str(json_data))
        email = json_data.email

        db_student = session.query(Student).filter(Student.email == email).first()
        if db_student:
            logger.info("Student Found")
            OTP = 123456
            logger.info("otp :: " + str(OTP))

            db_student_otp = session.query(StudentOtp).filter(
                StudentOtp.email == email).first()
            
            if not db_student_otp:
                new_otp = StudentOtp(
                    email=email,
                    otp=OTP)
                session.add(new_otp)
                logger.info("otp added")
                session.commit()

            else:
                expire_minutes_before = datetime.utcnow() - timedelta(minutes=15)
                logger.info("expire_minutes_before: " + str(expire_minutes_before))
                otp_created = db_student_otp.created.replace(tzinfo=None)

                # check if the email otp has expired or not
                if (otp_created >= expire_minutes_before):
                    logger.info('OTP EXISTS')
                    OTP = db_student_otp.otp
                    session.commit()
                else:
                    logger.info("OTP expired , generate new otp")
                    # email_otp = OTP
                    db_student_otp.email_otp = OTP
                    db_student_otp.created = datetime.utcnow()
                    session.commit()


            res_status = True
            res_message = SUCC_DEFAULT
            logger.info(res_message)
            status_code = 200
            return JSONResponse({
                'status': res_status,
                'email': db_student.email,
                'status_code': status_code,
            }, status_code=status_code)

        else:
            res_status = False
            res_message = ERR_ADMIN_NOT_FOUND
            logger.error(res_message)
            status_code = 400
            return JSONResponse({
                'status': res_status,
                'message': res_message,
                'status_code': status_code,
            }, status_code=status_code)

    except Exception as e:
        session.rollback()
        res_status = False
        res_message = ERR_SOMETHING_WENT_WRONG
        logger.error(res_message + " :: " + str(e))
        status_code = 500
        return JSONResponse({
            'status': res_status,
            'message': res_message,
            'status_code': status_code,
        }, status_code=status_code)


@router.post("/verify-otp")
def VerifyOTP(json_data: ValidateVerifyOTP):
    try:
        logger.info(f"Verify OTP - API :: email={json_data.email} otp={json_data.otp}")

        email = json_data.email
        otp = json_data.otp
        db_student = session.query(Student).filter(Student.email == email).first()
        if not db_student:
            logger.info(f"Student Not Found")
            res_status = False
            res_message = "Invalid Student."
            logger.error(res_message)
            status_code = 400
            return JSONResponse({
                'status': res_status,
                'message': res_message,
                'status_code': status_code,
            }, status_code=status_code)
        
        if db_student.active:
            # Otp check in otp with the email
                # if record -> check otp
                    # check validity
                        #  return true
                    # return expired
                # incorrect otp
            # invalid otp
            logger.info(f"Student Found")

            db_student_otp=session.query(StudentOtp).filter(StudentOtp.email== email).first()
            if db_student_otp:
                logger.info(f"Student Record exists")
                print(f"{db_student_otp.otp} == {otp}:")
                if db_student_otp.otp == otp:
                    logger.info(f"Otp is same as given")
                    expire_time = db_student_otp.created + timedelta(minutes=15)

                    if (datetime.utcnow() <= expire_time):
                        logger.info('OTP is valid')
                        res_status = True
                        res_message = SUCC_DEFAULT
                        logger.info(res_message)
                        status_code = 200
                        return JSONResponse({
                            'status': res_status,
                            'email': db_student.email,
                            'status_code': status_code,
                        }, status_code=status_code)
                    else:
                        logger.info("OTP expired , generate new otp")
                        db_student_otp.email_otp = otp
                        db_student_otp.created = datetime.utcnow()
                        session.commit()

                        res_status = False
                        res_message = "OTP has expired. Please request a new OTP."
                        logger.error(res_message)
                        status_code = 400
                        return JSONResponse({
                            'status': res_status,
                            'message': res_message,
                            'status_code': status_code,
                        }, status_code=status_code)
                
                else:
                    logger.info("OTP is incorrect")
                       
                    res_status = False
                    res_message = "OTP has Incorrect."
                    logger.error(res_message)
                    status_code = 400
                    return JSONResponse({
                        'status': res_status,
                        'message': res_message,
                        'status_code': status_code,
                    }, status_code=status_code)
         
            else:
                    res_status = False
                    res_message = "Invalid OTP"
                    logger.error(res_message)
                    status_code = 400
                    return JSONResponse({
                        'status': res_status,
                        'message': res_message,
                        'status_code': status_code,
                    }, status_code=status_code)
        else:
            res_status = False
            res_message = "Inactive student."
            logger.error(res_message)
            status_code = 401
            return JSONResponse({
                'status': res_status,
                'message': res_message,
                'status_code': status_code,
            }, status_code=status_code)
    except Exception as e:
        session.rollback()
        res_status = False
        res_message = ERR_SOMETHING_WENT_WRONG
        logger.error(f"{res_message} :: {str(e)}")
        status_code = 500
        return JSONResponse({
            'status': res_status,
            'message': res_message,
            'status_code': status_code,
        }, status_code=status_code)  


''' Reset Password'''
@router.post("/reset-password")
def Reset_Password(json_data: ValidateResetPassword):
    try:
        logger.info("Reset password - API :: "+str(json_data))
        email = json_data.email
        password = json_data.password
        db_student = session.query(Student).filter(Student.email == email).first()
        if db_student:
            logger.info(f"Student found")
            if db_student.active == True:

                salt = db_student.salt
                cf = AESCipher(salt, password)
                decrypted_value = cf.decrypt(db_student.encrypted_password)  # decrypt the password in the db
                logger.info(f"Decrypted Value : {decrypted_value}")
                if decrypted_value != password:
                    salt = os.urandom(8)
                    cf = AESCipher(salt, password)
                    encrypted_value = cf.encrypt(str(password)) 
                    db_student.encrypted_password = encrypted_value
                    db_student.salt = salt
                    db_student.updated = datetime.now()
                    session.commit()
                    logger.info(f"Password saved")

                    res_status = True
                    res_message = SUCC_DEFAULT
                    logger.info(res_message)
                    status_code = 200
                    return JSONResponse({
                            'status': res_status,
                            'email': db_student.email,
                            'status_code': status_code,
                    }, status_code=status_code)
                
                else:
                    logger.info(f"Current password is same as old password")
                    res_status = False
                    res_message = "Invalid Password"
                    logger.error(res_message)
                    status_code = 400
                    return JSONResponse({
                        'status': res_status,
                        'message': res_message,
                        'status_code': status_code,
                    }, status_code=status_code)
            else:
                res_status = False
                res_message = "Inactive student."
                logger.error(res_message)
                status_code = 400
                return JSONResponse({
                    'status': res_status,
                    'message': res_message,
                    'status_code': status_code,
                }, status_code=status_code)
        else:
            logger.info(f"Student Not Found")
            res_status = False
            res_message = "Invalid Student."
            logger.error(res_message)
            status_code = 400
            return JSONResponse({
                'status': res_status,
                'message': res_message,
                'status_code': status_code,
            }, status_code=status_code)
    
    except Exception as e:
        session.rollback()
        res_status = False
        res_message = ERR_SOMETHING_WENT_WRONG
        logger.error(f"{res_message} :: {str(e)}")
        status_code = 500
        return JSONResponse({
            'status': res_status,
            'message': res_message,
            'status_code': status_code,
        }, status_code=status_code)




# # Reset password
# @router.post("/student/reset-password")
# def reset_password(data: ResetPassword):
#     session = Session(engine)
#     student = session.query(Student).filter(Student.email == data.email).first()

#     if not student:
#         return {"error": "Student not found"}
#     if student.otp != data.otp:
#         return {"error": "Invalid OTP"}

#     student.password = hash_password(data.new_password)
#     student.otp = None
#     student.updated = datetime.now()
#     session.commit()
#     return {"message": "Password reset successful"}