year = 1
slow = 1000
fast = 1
death_slow = 0.4
death_fast = 0.3

print "+------+------------+------------+"
print "| Year |    Slow    |    Fast    |"
print "+------+------------+------------+"
while True:
    slow *= 2
    slow *= (1 - death_slow)
    fast *= 2
    fast *= (1 - death_fast)
    
    print "| %4d | %10.2f | %10.2f |" % (
        year, slow, fast)
    if fast > slow:
        break
    year += 1

print "+------+------------+------------+"
