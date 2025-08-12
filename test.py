# import pdfkit




# def generate_pdf(html_content,name='generated_pdf'):
#     config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
#     pdfkit.from_string(html_content,name+".pdf", configuration=config)
#     print("PDF created: invoice.pdf")


# with open('report.html', 'r', encoding='utf-8') as f:
#         content = f.read()
#         generate_pdf(content, name='invoice')


import pdfkit
from jinja2 import Environment, FileSystemLoader
from project.model.models import *

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('student_info.html')

def generate_pdf(data, name='generated_pdf'):
    config = pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
    pdfkit.from_string(data,name+".pdf", configuration=config)
    print("PDF created: student_info.pdf")


with open('student_info.html', 'r', encoding='utf-8') as f:
        content = f.read()
        generate_pdf(content, name='student_info')

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

print(data)

html_content = template.render(students=data)
generate_pdf(html_content, name='student_info')