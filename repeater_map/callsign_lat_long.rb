#!/usr/bin/ruby

file_name = 'qqq' 
`wget https://www.qrzcq.com/call/#{ARGV[0]} --output-document=#{file_name} 2>/dev/null`

doc = `cat #{file_name}`
index = doc.index("Latitude")

mystring = ''

(35..44).each do | i |

    mystring << doc[i+index]

end

puts "Lat = " +  mystring

index = doc.index("Longitude")
mystring = '' 

(36..45).each do | i |

    mystring << doc[i+index]

end

puts "Long = "+mystring
