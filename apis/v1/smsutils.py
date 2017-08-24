import requests
import furl

class SMSUtils:
  base_url = "https://control.msg91.com/api/sendhttp.php?authkey=170924AVVY9mnjELO599abb40&sender=Trapigo&route=1&country=India&"

  @classmethod
  def send_sms(cls, numbers, message, campaign='default'):
    f = furl.furl(cls.base_url)
    f.add({
      "mobiles": numbers,
      "campaign": campaign,
      "message": message,
    })
    print(f.url)


    #requests.get("https://control.msg91.com/api/sendhttp.php?authkey=170924AVVY9mnjELO599abb40&mobiles=7021835630&message=hello%20mayank%20how%20are%20you&sender=Trapigo&route=1&country=India&campaign=Test%20Campaign")
    
