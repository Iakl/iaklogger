import iaklogger as lg

lg.OPTIONS.allowed_tags = ["IAKL", "LOSA"]
lg.OPTIONS.show_tags = True
lg.OPTIONS.log_file = "log.txt"

lg.log("Hi everyone, I will record this conversation")
lg.log("Hi Default, Ok", tags=["IAKL", "CONVERSATION"])
lg.log("Hi Default, Ok for me too", tags=["LOSA", "CONVERSATION"])

lg.OPTIONS.allowed_tags = ["IAKL", "LOSA", "CONVERSATION"]
lg.OPTIONS.show_time = True

lg.log("Ok Iakl, you start")
lg.log("No no, you Losa", tags=["IAKL", "CONVERSATION"])
lg.log("Why me? you Default", tags=["LOSA", "CONVERSATION"])

# output: Hi! This prints by default

# allowed_tags = [
#     "PROCESS",
#     "DEBUG"
# ]

# lg.OPTIONS.allowed_tags = allowed_tags
# lg.OPTIONS.show_tags = True
# lg.OPTIONS.mute_default = True
# lg.OPTIONS.mute_all = True
# lg.OPTIONS.log_file = "log.txt"
# lg.OPTIONS.log_file_max_size_mb = 0.1
# # lg.OPTIONS.show_time = True

# lg.log("Hello World")
# lg.log("Hello World", tags=["PROCESS", "DEBUG"])
