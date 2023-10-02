from plyer import notification

def send_notification(title, message):
    notification_title = title 
    notification_message = message 
    
    notification.notify(  
        title = notification_title,  
        message = notification_message,  
        app_icon = None,  
        timeout = 10,  
        toast = True,
        )