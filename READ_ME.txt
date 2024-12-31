to use  
pip install -r requirements.txt




uplodat sheet steps 
1 - get url "upload_from_vue"  path invoice views 
load vue js page  invoice_vue.html 
use js functioon post to auth

use python function  upload_vue
    use function  create_request to create invoice on the current database 


usage 
1 - Create env 
2 - pip install -r windows_requirements.txt 
3-  python manage.py makemigrations & migrate 
4 - set Payer Account Data 
5 - python manage.py migrate 
6 - python run.py 