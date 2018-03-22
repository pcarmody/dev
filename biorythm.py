import datetime

today = datetime.date.today()
birthday = datetime.date(1962, 11, 14)
diff = today - birthday
mod = diff.days % 53
degrees = mod * 360 / 53

print "You have been alive "+repr(diff.days)+" days"
print "And you are at "+str(mod)+ " mod"
print "And you are at "+str(degrees)+ " degrees"
