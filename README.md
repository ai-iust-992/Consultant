# Consultant


error: 
    OperationalError at /admin/login/


You can use postgresql:

In settings.py add(at the end of file):

# ie if Heroku server
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config()}
In requirements.txt add:

dj-database-url 
psycopg2
Now you can run: heroku run python manage.py migrate




Heroku admin page:
admin
admin.iust.ac.ir
admin12345

rest_framework_swagger was old => dead => not support
