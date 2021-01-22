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
    Address="DEFAULT",
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
        return (False, str(e))
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
        return (False, str(e), None)
    raw_user = cur.fetchone()
    cur.close()
    conn.close()
    if raw_user:
        if check_password_hash(raw_user.pop("Password"), Password):
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
        return (False, str(e), None)
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
        return (False, str(e), None)
    raw_user = cur.fetchone()
    cur.close()
    conn.close()
    if raw_user:
        raw_user.pop("Password")
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
    Address="DEFAULT",
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
    try:
        cur.execute(sql_str)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e))
    cur.close()
    conn.close()
    return (True, "User profile updated successfully.")


def create_cluster(Name):
    """
    CREATE TABLE Clusters (
        ID INT NOT NULL AUTO_INCREMENT,
        Name VARCHAR(64) NOT NULL UNIQUE,
        PRIMARY KEY (ID)
    );
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        INSERT INTO Clusters (Name)
        VALUES ('{Name}')
    """
    try:
        cur.execute(sql_str)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e))
    cur.close()
    conn.close()
    return (True, "Cluster created successfully.")


def create_manager_cluster(ManagerID, ClusterID):
    """
    CREATE TABLE ManagerCluster (
        ManagerID INT NOT NULL,
        ClusterID INT NOT NULL,
        PRIMARY KEY (ManagerID, ClusterID),
        FOREIGN KEY (ManagerID) REFERENCES Users(ID)
        ON DELETE RESTRICT,
        FOREIGN KEY (ClusterID) REFERENCES Clusters(ID)
        ON DELETE RESTRICT
    )
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        INSERT INTO ManagerCluster
        (ManagerID, ClusterID)
        VALUES
        ({ManagerID}, {ClusterID})
    """
    try:
        cur.execute(sql_str)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e))
    cur.close()
    conn.close()
    return (True, "Cluster manager created successfully.")


def get_cluster_manager_list(ManagerID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT Name AS 'Cluster Name', ID AS 'Cluster ID'
        FROM Clusters WHERE ID IN
            (SELECT ClusterID
            FROM ManagerCluster
            WHERE ManagerID={ManagerID})
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    cluster_manager_list = cur.fetchall()
    cur.close()
    conn.close()
    return (
        True,
        "Manager's clusters retrieved from db, successfully",
        cluster_manager_list,
    )


def is_manager(UserID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT COUNT(1) AS is_manager
        FROM ManagerCluster
        WHERE ManagerID={UserID}
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    manager = cur.fetchone()
    cur.close()
    conn.close()
    return (
        True,
        "User checked for manager successfully",
        bool(int(manager["is_manager"])),
    )


def get_cluster_list(ManagerID, is_admin=False):
    if is_admin:
        return get_all_cluster_list()
    return get_cluster_manager_list(ManagerID)


def get_all_cluster_list():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = """
        SELECT Name AS 'Cluster Name', ID AS 'Cluster ID'
        FROM Clusters
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    cluster_list = cur.fetchall()
    cur.close()
    conn.close()
    return (True, "Clusters retrieved from db, successfully.", cluster_list)


def create_course(Name, TeacherID, ClusterID):
    """
    CREATE TABLE Courses (
        ID INT NOT NULL AUTO_INCREMENT,
        Name VARCHAR(64) NOT NULL,
        ClusterID INT NOT NULL,
        TeacherID INT NOT NULL,
        PRIMARY KEY (ID),
        FOREIGN KEY (ClusterID) REFERENCES Clusters(ID)
        ON DELETE RESTRICT,
        FOREIGN KEY (TeacherID) REFERENCES Users(ID)
        ON DELETE RESTRICT
    );
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        INSERT INTO Courses
        (Name, ClusterID, TeacherID)
        VALUES
        ('{Name}', {ClusterID}, {TeacherID})
    """
    try:
        cur.execute(sql_str)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e))
    cur.close()
    conn.close()
    return (True, "Course created successfully.")


def get_all_course_list():
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = """
        SELECT Name, ClusterID, TeacherID, ID
        FROM Courses
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e))
    course_list = cur.fetchall()
    cur.close()
    conn.close()
    return (True, "Course list retrieved from db, successfully", course_list)


def create_student_course(StudentID, CourseID):
    """
    CREATE TABLE StudentCourse (
        StudentID INT NOT NULL,
        CourseID INT NOT NULL,
        PRIMARY KEY (StudentID, CourseID),
        FOREIGN KEY (StudentID) REFERENCES Users(ID)
        ON DELETE RESTRICT,
        FOREIGN KEY (CourseID) REFERENCES Courses(ID)
        ON DELETE RESTRICT
    );
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        INSERT INTO StudentCourse
        (StudentID, CourseID)
        VALUES
        ({StudentID}, {CourseID})
    """
    try:
        cur.execute(sql_str)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e))
    cur.close()
    conn.close()
    return (True, "Student participated in the course successfully.")


def get_student_course_list(StudentID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT c.Name AS 'Course Name', u.FirstName AS 'Teacher First Name',
        u.LastName AS 'Teacher Last Name', c.ID AS 'Course ID'
        FROM ((StudentCourse AS sc
            INNER JOIN Courses AS c ON sc.CourseID = c.ID)
            INNER JOIN Users AS u ON c.TeacherID = u.ID)
        WHERE sc.StudentID = {StudentID}
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    student_course_list = cur.fetchall()
    cur.close()
    conn.close()
    return (True, "Courses retrieved from db, successfully.", student_course_list)


def get_teacher_course_list(TeacherID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT c.Name AS 'Course Name', u.FirstName AS 'Teacher First Name',
        u.LastName AS 'Teacher Last Name', c.ID AS 'Course ID'
        FROM Courses AS c
            INNER JOIN Users AS u ON c.TeacherID = u.ID
        WHERE c.TeacherID = {TeacherID}
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    teacher_course_list = cur.fetchall()
    cur.close()
    conn.close()
    return (True, "Courses retrieved from db, successfully.", teacher_course_list)


def is_teacher(UserID, CourseID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT COUNT(1) AS is_teacher
        FROM Courses
        WHERE ID={CourseID} AND TeacherID={UserID}
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    teacher = cur.fetchone()
    cur.close()
    conn.close()
    return (
        True,
        "User checked for teacher successfully",
        bool(int(teacher["is_teacher"])),
    )


def get_course(CourseID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT ID AS 'Course ID', Name AS 'Course Name', TeacherID AS 'Teacher ID'
        FROM Courses
        WHERE ID = {CourseID}
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    course = cur.fetchone()
    cur.close()
    conn.close()
    return (True, "Course retrieved from db, successfully", course)


def create_content(CourseID, Title, TextContent):
    """
    CREATE TABLE Contents (
        ID INT NOT NULL AUTO_INCREMENT,
        CourseID INT NOT NULL,
        Title VARCHAR(255) NOT NULL,
        TextContent LONGTEXT,
        CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (ID),
        FOREIGN KEY (CourseID) REFERENCES Courses(ID)
        ON DELETE RESTRICT
    );
    """
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        INSERT INTO Contents
        (CourseID, Title, TextContent)
        VALUES
        ({CourseID}, '{Title}', '{TextContent}')
    """
    try:
        cur.execute(sql_str)
        conn.commit()
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e))
    cur.close()
    conn.close()
    return (True, "Content created successfully.")


def get_content_list(CourseID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT Title, TextContent, CreatedAt
        FROM Contents
        WHERE CourseID = {CourseID}
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    content_list = cur.fetchall()
    cur.close()
    conn.close()
    return (True, "Contents retrieved from db, successfully", content_list)


def get_course_student_list(CourseID):
    conn = get_conn()
    cur = conn.cursor(dictionary=True)
    sql_str = f"""
        SELECT Username, FirstName AS 'First Name', LastName AS 'Last Name',
        PhoneNumber AS 'Phone Number', Email, Faculty
        FROM Users
        WHERE ID IN
        (SELECT StudentID FROM StudentCourse
        WHERE CourseID = {CourseID})
    """
    try:
        cur.execute(sql_str)
    except Error as e:
        cur.close()
        conn.close()
        return (False, str(e), None)
    student_list = cur.fetchall()
    cur.close()
    conn.close()
    return (True, "Student list retrieved from db, successfully", student_list)
