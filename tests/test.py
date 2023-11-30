from cvss4py import score_vector

vect1 = "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N/AU:N/R:U"
vect1_score = 6.9

vect2 = "CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:H/SC:H/SI:H/SA:L/E:P/CR:M/AR:M"
vect2_score = 5.7

print(vect1_score, score_vector(vect1))
print(vect2_score, score_vector(vect2))