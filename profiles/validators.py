import os
if os.path.exists("env.py"):
    import env


def validate_audiofile(filename):
    allowed_extensions = list(os.environ.get("ALLOWED_AUDIOFILE_EXTENSIONS").split(","))
    allowed_extensions = [x.strip(" ") for x in allowed_extensions]

    if filename != "":
        return "." in filename and filename.rsplit(
            ".", 1)[1].lower() in allowed_extensions
