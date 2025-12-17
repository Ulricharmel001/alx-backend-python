# Signal to send notification
Added a new signal in signals.py file that help to notify every participant in a conversation 
when ever message is sent, notification of message is sent to all except the sender 

# Signal to log History odf edited Messages

This particular signal help to log all the history of edited messages in a chat 

# Feature to delete user account
 This feature allow uswrs to delete their account 
 it also contain a signal that immediatelly alert, the other instances
 the signal auto automatically triggered action to delete all nofication of that  user also messages


 # New field in Message model
 this help to indicate if message has been read or not 
 also implemented the .only key word in my query this help to limit fields to query 

# Caching of dataa
Implement caching using djangoresframework to optimize data response and query time