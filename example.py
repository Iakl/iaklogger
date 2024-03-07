import iaklogger as lg

allowed_tags = [
    "PROCESS",
    "DEBUG"
]

lg.OPTIONS.allowed_tags = allowed_tags
lg.OPTIONS.show_tags = True
# lg.OPTIONS.mute_default = True
# lg.OPTIONS.mute_all = True
lg.OPTIONS.log_file = "log.txt"
lg.OPTIONS.log_file_max_size_mb = 0.1
# lg.OPTIONS.show_time = True

lg.log("Hello World")
lg.log("Hello World", tags=["PROCESS", "DEBUG"])
