## Building a new LAMP (Linux, Apache, MySQL, PHP) environment while carrying over existing data involves a few crucial steps. 

This guide assumes you have SSH access to both your existing and new servers and that you have sudo privileges.

* * *

### Part 1: Backup Existing Data

#### Step 1: SSH into Existing Server

-   Use SSH to connect to your existing server.
        
    `ssh username@your_server_ip_address` 
    

#### Step 2: Backup MySQL Databases

1.  Log in to MySQL:
    
    `mysql -u root -p` 
    
    You'll be prompted to enter the MySQL root password.
    
2.  Create a backup for each database using `mysqldump`:
    
	    mysqldump -u root -p vtartsalon_db > ~/vtartsalon_db.sql
	    mysqldump -u root -p husart_db > ~/husart_db.sql
    
    You'll be prompted to enter the MySQL root password each time.
    
3.  Exit MySQL:
    
    `exit` 
    

#### Step 3: Archive Web Files

1.  Navigate to the `/var/www/` directory.
    
    `cd /var/www/` 
    
2.  Archive each WordPress site's directory:
    
	    sudo tar -czvf ~/vtartsalon.tar.gz vtartsalon/
	    sudo tar -czvf ~/husart.tar.gz husart/
    

#### Step 4: Transfer Backup Files

-   Use SCP to transfer the backup SQL and tar.gz files to a local or remote safe location.
    
	    scp ~/vtartsalon_db.sql username@backup_server:/path/to/backup/
	    scp ~/husart_db.sql username@backup_server:/path/to/backup/
	    scp ~/vtartsalon.tar.gz username@backup_server:/path/to/backup/
	    scp ~/husart.tar.gz username@backup_server:/path/to/backup/
    

* * *

### Part 2: Set Up a New LAMP Server

#### Step 5: Create a New GCP LAMP Instance

-   Go to Google Cloud Platform Console and create a new LAMP Stack instance.

#### Step 6: SSH into the New Server

-   Use SSH to connect to your new server.
    
    `ssh username@new_server_ip_address` 
    

#### Step 7: Update and Install Essential Packages

-   Update the package list and install the essential LAMP packages.
    
	    sudo apt update
	    sudo apt install apache2 mysql-server php
	    

* * *

### Part 3: Restore Data and Configuration

#### Step 8: Restore MySQL Databases

1.  Transfer the SQL backup files to the new server using SCP or another secure method.
       
	    scp username@backup_server:/path/to/backup/vtartsalon_db.sql ~/
	    scp username@backup_server:/path/to/backup/husart_db.sql ~/
    
2.  Log in to MySQL:
    
    `mysql -u root -p` 
    
    You'll be prompted to enter the MySQL root password.
    
3.  Create new databases:
    
    CREATE DATABASE new_vtartsalon_db;
    CREATE DATABASE new_husart_db;
    
4.  Import the backup data:
   
	    mysql -u root -p new_vtartsalon_db < ~/vtartsalon_db.sql
	    mysql -u root -p new_husart_db < ~/husart_db.sql
    
5.  Exit MySQL:
    
    `exit` 
    

#### Step 9: Restore Web Files

1.  Transfer the backup tar.gz files to your new server.
    
	    scp username@backup_server:/path/to/backup/vtartsalon.tar.gz ~/
	    scp username@backup_server:/path/to/backup/husart.tar.gz ~/
	    
2.  Extract the backups in `/var/www/`:
    
	    sudo tar -xzvf ~/vtartsalon.tar.gz -C /var/www/
	    sudo tar -xzvf ~/husart.tar.gz -C /var/www/
    

#### Step 10: Configure Apache Virtual Hosts

-   Create new Apache config files for each site, and edit them according to your new setup.
    
    
	    sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/vtartsalon.conf
	    sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/husart.conf
	    sudo nano /etc/apache2/sites-available/vtartsalon.conf
	    sudo nano /etc/apache2/sites-available/husart.conf
    

#### Step 11: Enable Sites and Reload Apache

-   Enable the Apache sites and reload Apache.
    
    
	    sudo a2ensite vtartsalon.conf
	    sudo a2ensite husart.conf
	    sudo systemctl reload apache2
	    

#### Step 12: Install SSL Certificates

-   Use Certbot to install new SSL certificates.
        
	    sudo apt install certbot python3-certbot-apache
	    sudo certbot --apache
    

#### Step 13: Test Websites

-   Open a web browser and navigate to your websites to confirm they are working as expected.
