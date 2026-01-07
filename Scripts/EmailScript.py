'''Directly connect to Gmail mail server, where Gmail will be the "transport", send the email after writing logic'''

#for email sending 
import smtplib
#for email formating 
from email.mime.text import MIMEText
#get email information  from config file
from config import SMTP_SERVER, SMTP_PORT, USERNAME, PASSWORD, RECEIVER, SUMMARIES_ROOT
from context import ctx
from pathlib import Path


def get_summary_files(start_utc_time: str) -> list[str]:
    """ Get the summary file paths from SUMMARIES_ROOT """
    summary_folder = Path(SUMMARIES_ROOT) / ctx.start_utc_time
    return [str(p) for p in summary_folder.glob("*")]


def load_summaries(summary_file: str):
    """ Load the summary files from the SUMMARIES_ROOT """
    return Path(summary_file).read_text(encoding="utf-8")


def build_daily_body(summary_files: list[str]) -> str:
    """ Concatenate all summaries into a single plain-text body.
    Adds a header and per-file separators for readability."""
    body = []
    for summary_file in summary_files:
        summary_text = load_summaries(summary_file).strip()
        body.append(f"--- Summary for {Path(summary_file).name} ---")
        body.append(summary_text)
    return "\n\n".join(body)


if __name__ == "__main__":
    
    summary_files = get_summary_files(ctx.start_utc_time)
    BODY = build_daily_body(summary_files)
    MESSAGE = MIMEText(BODY, "plain")
    #print(MESSAGE)

    MESSAGE["Subject"] = f"Article Summaries {ctx.start_utc_time}"
    MESSAGE["From"] = USERNAME
    MESSAGE["To"] = RECEIVER

    with smtplib.SMTP(SMTP_SERVER,SMTP_PORT, timeout = 10) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(USERNAME,PASSWORD)
        server.sendmail(USERNAME,[RECEIVER],MESSAGE.as_string())