# TheRiver
A python-based console **level chat application** with **local-level communication**.


## Get Started with  [TheRiver](https://github.com/TheGoodUser/TheRiver)
* The **TheRiver** contains mainly ```Server.py``` ,  ```@brook1```  and ```@brook2``` files, you can edit the names with you want to be connected. First you need to execute the ```python.exe server.py``` command which if says "SERVER LIVE" then its a one go, after that run the ```python.exe brook1.py``` command. These are the clients which will connect to each other through server and a message ![server live displaying image](https://i.postimg.cc/XXhgv6kr/brook-you-are-live.png) appears if everything goes fine.
* Add another client, just execute the another ```brook2.py``` file and start your chit-chatting, and if you want to add more clients, connect more friends with each just copy the brook.py and give it a name and enter  the same command again.


## Record Keeping
* Every message transmitted is recorded in ```chat-history.txt``` file.
* The format of saving the records is (hostname, message, time).


## Libraries Used
**TheRiver** uses Python Standard Libraries :-
  - ```socket```  : for making tcp connections.    
  - ```threading``` : for handling multiple connection(s) simultaneously.
  - ```time``` : for maintaining record of each message.

**TheRiver** uses Third-Party Library :-
  - ```colorama``` :  for a colored terminal text. Can be installed using command ```pip install colorama```.

 


