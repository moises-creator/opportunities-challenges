#Baixe as dependências e execute o código :)

#host="localhost",
# user="yourusername",
# password="yourpassword",
# database="mydatabase" 
# Extrai-a do PDF anexo todos os emails e telefones  existentes, e depois os insira nesse DB fictício. Considere que ele está vazio. 

import PyPDF2
import mysql.connector
import re

REGEX_PHONE = "\(\d\d\)\s+\d\d\d\d\d-\d\d\d\d"
REGEX_EMAIL = "[\w.+-]+@[\w-]+\.[\w.-]+"

def connect_mysql(host="localhost", user="yourusername", password="yourpassword", database="mydatabase"):
    conn = mysql.connector.connect(host=host, user=user, password=password, database=database)
    if conn.is_connected():
        return conn
    else:
        return False

def create_tables_in_database():
    try:
        conn = connect_mysql()
        cursor = conn.cursor()
        #Supondo que não hajam emails maiores que 50 caracteres no arquivo e que todos os telefones tem 15 caracteres, contando o espaço e os parenteses.
        cursor.execute('CREATE TABLE IF NOT EXISTS emails (email VARCHAR(50))')
        cursor.execute('CREATE TABLE IF NOT EXISTS telefones (telefone VARCHAR(15))')
        conn.close()
        return True
    except:
        return False

def insert_data_into_table(table_name, column, data):
    try:
        conn = connect_mysql()
        cursor = conn.cursor()
        for item in data:
            cursor.execute(f'insert into {table_name} ({column}) VALUES ("{item}")')
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_set_from_pdf(file_name, str_pattern):
    pdfFile = open(file_name, 'rb')
    pdfRead = PyPDF2.PdfFileReader(pdfFile)
    n_pages = pdfRead.numPages
    pattern  = re.compile(str_pattern)
    obj_list = []
    for page in range(0, n_pages):
        pageObj = pdfRead.getPage(page)
        textPdf = pageObj.extractText()
        matches_in_page = pattern.findall(textPdf)
        if matches_in_page:
            obj_list += matches_in_page
    pdfFile.close()
    #A lista é convertida para set, para que as duplicatas sejam removidas
    obj_set = set(obj_list)
    return obj_set

def get_telefones():
    phone_set = get_set_from_pdf("dados.pdf", REGEX_PHONE)
    return phone_set

def get_emails():
    email_set = get_set_from_pdf("dados.pdf", REGEX_EMAIL)
    return email_set

def run():
    #Obtém emails do documento
    emails = get_emails()
    #Obtém telefones do documento
    telefones = get_telefones()
    #Cria tabelas no DB caso não existam
    if(create_tables_in_database()):
        #Insere dados extraídos na tabela de telefones
        if telefones:
            insert_data_into_table("telefones", "telefone", telefones)
        #Insere dados extraídos na tabela de emails
        if emails:
            insert_data_into_table("emails", "email", emails)
    else:
        print("Não foi possível acessar as tabelas para inserção")

if __name__ == "__main__":
    run()