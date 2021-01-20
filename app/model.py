from mysql.connector import connect, Error
from werkzeug.security import generate_password_hash, check_password_hash
from . import local_settings


def get_conn():
    conn = connect(
        host=local_settings.MYSQL_HOST,
        user=local_settings.MYSQL_USER,
        password=local_settings.MYSQL_PASSWORD,
        database=local_settings.MYSQL_DB,
    )
    return conn


def create_user(
    Username,
    Password,
    is_student="DEFAULT",
    is_teacher="DEFAULT",
    is_manager="DEFAULT",
    is_admin="DEFAULT",
    LastName="DEFAULT",
    FirstName="DEFAULT",
    PhoneNumber="DEFAULT",
    Email="DEFAULT",
    Faculty="DEFAULT",
    Institution="DEFAULT",
    Address="DEFAULT"
):
    """
    CREATE TABLE Users (
        ID INT NOT NULL AUTO_INCREMENT,
        Username VARCHAR(64) NOT NULL UNIQUE,
        Password VARCHAR(255) NOT NULL,
        is_student BOOLEAN DEFAULT false,
        is_teacher BOOLEAN DEFAULT false,
        is_manager BOOLEAN DEFAULT false,
        is_admin BOOLEAN DEFAULT false,
        LastName VARCHAR(255),
        FirstName VARCHAR(255),
        PhoneNumber CHAR(13),
        Email VARCHAR(320),
        Faculty VARCHAR(255),
        Institution VARCHAR(255),
        Address VARCHAR(2048),
        PRIMARY KEY (ID)
    );

    """
    if len(Username) < 4:
        error_message = "Username should be at least 4 characters long"
        return (False, error_message)
    if len(Password) < 6:
        error_message = "Password should be at least 6 characters long"
        return (False, error_message)
    conn = get_conn()
    cur = conn.cursor()
    Password = generate_password_hash(Password)
    sql_str = f"""
        INSERT INTO Users
        (Username, Password, is_student, is_teacher, is_manager, is_admin,
        LastName, FirstName, PhoneNumber, Email, Faculty, Institution, Address)
        VALUES
        ('{Username}', '{Password}', {is_student}, {is_teacher},
        {is_manager},{is_admin}, '{LastName}', '{FirstName}', '{PhoneNumber}',
        '{Email}', '{Faculty}', '{Institution}', '{Address}')
    """
    try:
        cur.execute(sql_str)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        return (False, e)
    cur.close()
    conn.close()
    return (True, f"User with username: {Username} created successfully")


def check_login(Username, Password):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT ID, Username, Password, FirstName, LastName,
        is_student, is_teacher, is_manager, is_admin
        FROM Users WHERE
        Username = '{Username}'
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, e, None)
    raw_user = cur.fetchone()
    cur.close()
    conn.close()
    if raw_user:
        if check_password_hash(raw_user.pop('Password'), Password):
            return (True, "Correct username and password", raw_user)
    return (False, "Wrong username or password", raw_user)


def get_user_list():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = """
        SELECT Username, FirstName AS 'First Name', LastName AS 'Last Name',
        PhoneNumber AS 'Phone Number', Email, Faculty, ID
        FROM Users
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, e, None)
    user_list = cur.fetchall()
    cur.close()
    conn.close()
    return (True, "User list retrieved from db, successfully", user_list)


def get_user_profile(ID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT *
        FROM Users
        WHERE ID={ID}
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, e, None)
    raw_user = cur.fetchone()
    cur.close()
    conn.close()
    if raw_user:
        raw_user.pop('Password')
        return (True, "User profile retrieved from db, successfully", raw_user)
    return (False, "No such user exists", None)


def edit_user_profile(
    ID,
    Username,
    LastName="DEFAULT",
    FirstName="DEFAULT",
    PhoneNumber="DEFAULT",
    Email="DEFAULT",
    Faculty="DEFAULT",
    Institution="DEFAULT",
    Address="DEFAULT"
):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        UPDATE Users
        SET LastName = '{LastName}', FirstName = '{FirstName}',
        PhoneNumber = '{PhoneNumber}', Email = '{Email}',
        Faculty = '{Faculty}', Institution = '{Institution}',
        Address = '{Address}', Username = '{Username}'
        WHERE ID = {ID};
    """
    print("----------------------------------------")
    print(sql_str)
    print("----------------------------------------")

    try:
        cur.execute(sql_str)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        return (False, e)
    return (True, "User profile updated successfully.")
