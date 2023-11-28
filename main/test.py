import _mysql_connector

import mysql.connector

# Connect to the MySQL database
connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Ideapad320@",
    database="capstone"
)

# Read the image file as binary data
def upload():
    with open('C:\\Users\\alliw\\Downloads\\80.webp', 'rb') as file:
        image_data = file.read()

    # Insert the image data into the database
    cursor = connection.cursor()
    query = "INSERT INTO cap (image, name) VALUES (%s, %s)"
    cursor.execute(query, (image_data, 'default.jpg'))
    connection.commit()

    # Close the connection
    connection.close()

def read():
    cursor = connection.cursor()
    image_id = 5  # Replace with the ID of the image you want to retrieve
    query = "SELECT image FROM cap WHERE idCap = %s"
    cursor.execute(query, (image_id,))
    image_data = cursor.fetchone()[0]

    # Save the image data to a file
    with open('retrieved_image.jpg', 'wb') as file:
        file.write(image_data)
    connection.close()

read()

