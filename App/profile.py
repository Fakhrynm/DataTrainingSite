import streamlit as st
import psycopg2
from PIL import Image
import io

def app():
    st.title("profile")

    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        user='postgres',
        password='admin',
        host='localhost',
        port='5432',
        database='Testing'
    )

    # Create a cursor object to execute queries
    cursor = connection.cursor()
   
    # Execute a query to retrieve the data
    cursor.execute("SELECT id, latitude, longitude, image_data FROM location_images")

    # Fetch all the rows returned by the query
    data = cursor.fetchall()

    # Display the data in Streamlit
    for row in data:
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
        with col1:
            st.write("ID:", row[0])
        with col2:
            st.write("Latitude:", row[1])
        with col3:
            st.write("Longitude:", row[2])
        with col4:
            # Check for null or empty image value
            if row[3] is not None and len(row[3]) > 0:
                # Convert bytea to PIL Image
                image_bytes = io.BytesIO(row[3])
                image = Image.open(image_bytes)
                st.image(image, use_column_width=True)
            else:
                st.write("No image available")

        # Allow the user to upload a new image
        new_image = st.file_uploader(f"Update Image for ID {row[0]}", type=["png", "jpg"])

        if new_image is not None:
            # Read the image data
            image_data = new_image.read()

            # Update the image in the database using SQL UPDATE statement
            id_to_update = row[0]
            cursor.execute("UPDATE location_images SET image_data = %s WHERE id = %s", (psycopg2.Binary(image_data), id_to_update))
            connection.commit()

            # Show a success message
            st.success("Image updated successfully!")

    # Close the cursor and connection
    cursor.close()
    connection.close()
