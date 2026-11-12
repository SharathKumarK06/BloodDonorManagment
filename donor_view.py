from mysql import connector
from datetime import datetime

class BloodDonorManager:
    def __init__(self):
        self.connection = connector.connect(
            user="sharath",
            password="mysql",
            host="localhost",
            db="blood_db"
        )
        if self.connection:
            print("Successfully connected to mysql.")
        self.cursor = self.connection.cursor()

    def post(self, **kwargs):
        values = [v for v in kwargs.values()]
        query = """
        insert into donor (name, blood_group, phone, city, last_donation)
        values (%s, %s, %s, %s, %s)
        """
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print("Data inserted successfully.")
        except Exception as e:
            print(e)

    def get_object(self, id=None):
        query = "select * from donor where id = %s"
        record = None
        try:
            self.cursor.execute(query, (id,))
            record = self.cursor.fetchone()
        except Exception as e:
            print(e)
        return record

    def get(self, id=None):
        if id == None:
            query = "select * from donor"
            records = []
            try:
                self.cursor.execute(query)
                records = self.cursor.fetchall()
                for r in records:
                    print(r)
            except Exception as e:
                print(e)
        else:           
            record = self.get_object(id)
            if not record:
                print("No donors found.")
            else:
                print(record)

    def delete(self, id=None):
        record = self.get_object(id)
        query = "delete from donor where id=%s"
        if record:
            self.cursor.execute(query, (id,))
            self.connection.commit()
            print("Donor deleted successfully.")
        else:
            print("No donors found.")

    def put(self, id=None, **kwargs):
        if not id:
            print("Error: id is not provided.")
        else:
            record = self.get_object(id)
            if not record:
                print("Error: record with id not found.")
                return
            placeholder = ""
            for k in kwargs.keys():
                placeholder += f"{k}=%s, "
            placeholder = placeholder.rstrip(", ")
            query = f"update donor set {placeholder} where id={id}"
            values = [v for v in kwargs.values()]
            
            try:

                self.cursor.execute(query, values)
                self.connection.commit()
                print("Donor updated successfully.")
            except Exception as e:
                print("Error:", e)

donor_manager = BloodDonorManager()
# donor 1
# donor_manager.post(
#     name="Rahul", blood_group="O+",
#     phone="+919088675634", city="Kakkanad",
#     last_donation=datetime.today()
# )
# donor 2
# donor_manager.delete(4)
# donor_manager.post(
#     name="Akshay", blood_group="O-",
#     phone="+919057674624", city="Kaloor",
#     last_donation=datetime.today()
# )
# donor_manager.put(5, last_donation=datetime.today())
donor_manager.get()
