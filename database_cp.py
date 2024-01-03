from abc import ABC  


class MySQL_processor(ABC):

    def __init__(self, time, name, seri_no, message):
        self.time = time
        self.name = name
        self.seri_no = seri_no
        self.message = message


class MySQL_processor_Port(MySQL_processor): 

    def __init__(self, time, port, name, seri_no, message):
        super().__init__(time, name, seri_no, message)

        self.port = port

        import mysql.connector  
        from mysql.connector import Error
        connection = mysql.connector.connect(host='localhost',
                                             db='comportlog',
                                             user='root',
                                             passwd='sspspsdps'
                                             )

        try:  
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)  
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)  

                cursor = connection.cursor()  

               
                sql = "INSERT INTO logtable(Time,Port,Name,Seri_No,Message) VALUES (%s,%s,%s,%s,%s)"
                values = (self.time, self.port, self.name, self.seri_no, self.message)

                cursor.execute(sql, values)  
                connection.commit()          

                # cursor.execute("CREATE DATABASE pydb")
                # cursor.execute("CREATE TABLE portlog (Time VARCHAR(255), Port VARCHAR(255), Name VARCHAR(255))")

                # cursor.execute("SHOW DATABASES")
                # for x in cursor:
                #     print(x)              # (şu yukarıdaki 6 satırı görmeyin, alakasız)

        except Error as e: 
            print("Error while connecting to MySQL", e)
        finally:  
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")


class MySQL_processor_USB(MySQL_processor): 
    def __init__(self, time, name, seri_no, vid, pid, message):
        super().__init__(time, name, seri_no, message)
        self.vid = vid
        self.pid = pid

        import mysql.connector
        from mysql.connector import Error
        connection = mysql.connector.connect(host='localhost',
                                             db='comportlog',
                                             user='root',
                                             passwd='1243564'
                                             )

        try:
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

                cursor = connection.cursor()

                sql = "INSERT INTO logtable(Time,Name,Seri_No,VID,PID,Message) VALUES (%s,%s,%s,%s,%s,%s)"
                values = (self.time, self.name, self.seri_no, self.vid, self.pid, self.message)

                cursor.execute(sql, values)
                connection.commit()

                # cursor.execute("CREATE DATABASE pydb")
                # cursor.execute("CREATE TABLE portlog (Time VARCHAR(255), Port VARCHAR(255), Name VARCHAR(255))")

                # cursor.execute("SHOW DATABASES")
                # for x in cursor:
                #     print(x)

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        # (host='192.168.1.***',
        # database='abdu**',
        # user='root',
        # password='servers**')



