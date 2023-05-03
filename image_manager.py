import database_operations as do

class image_manager:
    
    def upload(pictures: list):
        do.make_table('images', ['id INTEGER PRIMARY KEY', 'name varchar(30)'])

        # ... add virtual environment