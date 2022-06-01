# Instructions for the PI ACE Inventory App

1. PIacl.dat file needs to be taken backup of - can not do this manually when PI services are running
2. pimoduledb.dat file needs to be taken backup of - can not do this manually when PI services are running
3. Run a 'copy' backup of the dat folder only - In SMT (Can do this with the customer as part of prereq)
4. Pass the files to an SE (PIacl.dat and pimoduledb.dat)
5. Load the files in dedicated vm environment with 32bit excel and MDBBuilder - Extract everything in MDB
6. Save as a CSV
7. clone github 'https://github.com/mpucci92/PIACEInventoryApp.git' to access python directory
7. Open CSV and save as a CSV UTF8 file in the 'Data' folder
8. Run it through my python script and observe the 'Output' folder to view contents


Dependencies: Python 3.8.5+, PIP install Pandas, Numpy, glob2, DateTime
