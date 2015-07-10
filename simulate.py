qa = [0]
qb = [0]

alpha = 0.5
gamma = 0.75

ra = 0.2
rb = 0.2

max_sample = 40

final_qa = (ra + gamma * rb) / (1 - gamma ** 2)
final_qb = (rb + gamma * ra) / (1 - gamma ** 2)

print "final_qa: %s" % (final_qa)
print "final_qb: %s" % (final_qb)

for i in range(1, max_sample):
    # if i==12:
    # 	alpha*=0.5
    # if i==22:
    # 	alpha*=0.5
    # if i==30:
    # 	alpha*=0.5
    # if i==36:
    # 	alpha*=0.5
    if i%2==0:
    	alpha*=0.9
    if i % 2:
        length = len(qa)
        reward = (1 - alpha) * qa[length - 1] + \
            alpha * (ra + gamma * qb[len(qb) - 1])
        qa.append(reward)
    else:
        length = len(qb)
        reward = (1 - alpha) * qb[length - 1] + \
            alpha * (rb + gamma * qa[len(qa) - 1])
        qb.append(reward)
print qa
print qb

print "----------------------ratio------------------------"

ratio_qa = []
ratio_qb = []

sum_ratio_a = 0
sum_ratio_b = 0

for i in range(len(qa) - 1):
    ratio_qa.append((qa[i + 1] - qa[i]) / final_qa * 100)
    sum_ratio_a += ratio_qa[i]

for i in range(len(qb) - 1):
    ratio_qb.append((qb[i + 1] - qb[i]) / final_qb * 100)
    sum_ratio_b += ratio_qb[i]


print ratio_qa
print sum_ratio_a

print ratio_qb
print sum_ratio_b