from fastapi import APIRouter,Depends
from fastapi.responses import JSONResponse
from project.model.models import *
from datetime import datetime
from project.config.error_messages import *
from project.component.token import validate_student_access_token



router=APIRouter(prefix='/api/v1/student')
logger = set_up_logging()


'''Create a new student'''

@router.post("/create")
def create_student(json_data: ValidateStudentCreate):
    try:
        logger.info("[Add student - API]")
        logger.info("cyril deleted this change from cyril-dev")
        fname=json_data.fname
        lname=json_data.lname
        mobile=json_data.mobile
        email=json_data.email
        created=datetime.now()
        updated=datetime.now()

        db_newstudent = session.query(Student).filter(
            Student.email == email).first() # check if email exists for student
        if not db_newstudent:
            new_student = Student(
                email=email,
                fname=fname,
                lname=lname,
                mobile=mobile,
                active = True,
                created = created,
                updated = updated)
            
            logger.info(new_student)
            session.add(new_student)
            session.commit()

            res_status = True
            res_message = SUCC_DEFAULT
            logger.info(res_message)
            status_code = 200

            return JSONResponse({
                'status': res_status,
                'status_code': status_code,
                'message': res_message,
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


''' List students '''
@router.get("/list")
def list_student(stud_id:int = Depends(validate_student_access_token)):
    if stud_id:
        try:
            db_student = session.query(Student).filter(Student.active == True).all()
            data = []

            for s in db_student:
                temp_data = {}
                temp_data["id"] = s.id
                temp_data["fname"] = s.fname
                temp_data["lname"] = s.lname
                temp_data["email"] = s.email
                temp_data["mobile"] = s.mobile
                data.append(temp_data)

            res_status = True
            res_message = SUCC_DEFAULT
            logger.info(res_message)
            status_code = 200

            return JSONResponse({
                'status': res_status,
                'status_code': status_code,
                'message': res_message,
                'data': data
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
    else:
        res_status = False
        res_message = "Invalid Token"
        logger.info(res_message)
        status_code = 401
        return JSONResponse({
            'status': res_status,
            'status_code': status_code,
            'message': res_message
        }, status_code=status_code)


''' Update student '''
@router.put("/update")
def update_student(json_data: ValidateStudentCreate):
    try:
        logger.info("Update student")
        id = json_data.id
        fname=json_data.fname
        lname=json_data.lname
        mobile=json_data.mobile
        email=json_data.email
        updated=datetime.now()

        print(type(fname))

        db_student = session.query(Student).filter(
            Student.id == id).first() # check if id exists for student
        if db_student:
            logger.info(f"Student found with name {db_student.fname}")
            db_student.fname = fname
            db_student.lname = lname
            db_student.mobile = mobile
            db_student.email = email
            db_student.updated = updated

            session.commit()

            res_status = True
            res_message = SUCC_DEFAULT
            logger.info(res_message)
            status_code = 200

            return JSONResponse({
                'status': res_status,
                'status_code': status_code,
                'message': res_message,
            }, status_code=status_code)

        else:
            res_status = False
            res_message = ERR_STUDENT_NOT_FOUND
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

''' Deactivate student '''
@router.delete("/delete")
def delete_student(json_data: validateDeleteStudent):
    try:
        logger.info("delete student")
        id = json_data.id

        db_student = session.query(Student).filter(
            Student.id == id).first() # check if id exists for student
        if db_student:
            logger.info(f"Student found with name {db_student.fname}")
            db_student.active = False
            session.commit()

            res_status = True
            res_message = SUCC_DEFAULT
            logger.info(res_message)
            status_code = 200

            return JSONResponse({
                'status': res_status,
                'status_code': status_code,
                'message': res_message,
            }, status_code=status_code)

        else:
            res_status = False
            res_message = ERR_STUDENT_NOT_FOUND
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
    
