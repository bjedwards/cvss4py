from cvss4py import score_vector

test_vects = [
    {
        "v":"CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:N/VI:N/VA:N/SC:N/SI:L/SA:N/AU:N/R:U",
        "s": 6.9
    },
    {
        "v":"CVSS:4.0/AV:A/AC:L/AT:N/PR:N/UI:P/VC:H/VI:L/VA:H/SC:H/SI:H/SA:L/E:P/CR:M/AR:M",
        "s": 5.7
    },
    {
        "v":"CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:H/SI:H/SA:H/E:P/CR:H/IR:L/AR:M/MAV:N/MAT:N/MUI:P/MVA:L/MSC:H/MSI:L/MSA:S/S:P/AU:N/R:I/V:C/RE:H/U:Amber",
        "s":9.3
    }
]

for d in test_vects:
    print(d['s'], score_vector(d['v'],  warn_modified=False))