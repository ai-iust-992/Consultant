# Consultant



Heroku admin page:
admin
admin.iust.ac.ir
admin12345


python manage.py makemigrations User calendar_ channel chat_room message 


add ('auth', '__latest__') to dependency of migrations 



see django sqlite db:
sqlite3 db.sqlite3
.tables

SELECT sql FROM sqlite_master WHERE tbl_name = 'channel_channel' AND type = 'table'



# search-for-channel : 
http://localhost:8000/channel/search-for-channel/?query=&search_category=Lawyer    : return all channel in Lawyer category

http://localhost:8000/channel/search-for-channel/?query=         : return all channel



# problem :
1- In get channel subscribers:  API is just for channel owner and admin   
2- channel has not avatar 
3- searchs API han not return avatar of channels