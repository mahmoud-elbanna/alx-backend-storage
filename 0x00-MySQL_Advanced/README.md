# -0x00-MySQL_Advanced
# -TASK O 
# - CREAT DATABASE holberton;
# - THEN CREAT A TABLE "USERS" IN THE PREVIOUS "DATABASE" WITHS THIS COLUMNS;
# - ID: INT  NOT NULL PRIMARY KEY AUTO_INCREMENT,
# - NAME: varchar(255),
# - EMAIL: varchar(255) NOT NULL UNIQUE,
# - THEN TO INSERT DATA TO THIS TABLE WE USE THIS COMMAND
# - "echo 'INSERT INTO USERS (EMAIL, NAME) VALUES ("EMAIL:VALUE", "NAME:VALUE");' | mysql -uroot -p "DATABASENAME" "
# - "echo "SELECT * FROM USERS;" | mysql -uroot -p "DATABASE NAME" " TO CHECK OUT THE RESULT

----------------------------------------------------------------------------------
# - TASK 1 
# - I USED ALTER TO ADD A COLUMN "country"
# -  LIKE THIS "ALTER TABLE "TABLE NAME"
#   ADD COLUMN country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL;"
# - AND USED THIS COMMAND "echo "SHOW FIELDS FROM "TABLE NAME" | mysql -uroot -p "D-B NAME" " TO CHECK OUT THE RESULT
# - AND UPDATE THE TABLE WITH THIS COMMAND echo 'UPDATE users SET name="VALUE", country="US" WHERE email="VALUE";' | mysql -uroot -p "D-B NAME "
# - TO KNOW ALL COLUMNS IN THE TABLE USE "DESCRIBE "TABLE NAME"; " OR  "SHOW COLUMNS FROM "TABLE NAME";"
-----------------------------------------------------------------------------------
