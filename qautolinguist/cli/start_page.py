"Startup page for QAutoLinguist CLI."

import click
import platform
import sys
from os import name, system
from datetime import datetime
from click import style, echo #, wrap_text, clear
from __version import __version__ as qal_version



_STARTUP_TITLE = r"""
________/\\\___________/\\\\\\\\\_____/\\\_____________        
 _____/\\\\/\\\\______/\\\\\\\\\\\\\__\/\\\_____________       
  ___/\\\//\////\\\___/\\\/////////\\\_\/\\\_____________      
   __/\\\______\//\\\_\/\\\_______\/\\\_\/\\\_____________     
    _\//\\\______/\\\__\/\\\\\\\\\\\\\\\_\/\\\_____________    
     __\///\\\\/\\\\/___\/\\\/////////\\\_\/\\\_____________   
      ____\////\\\//_____\/\\\_______\/\\\_\/\\\_____________  
       _______\///\\\\\\__\/\\\_______\/\\\_\/\\\\\\\\\\\\\\\_ 
        _________\//////___\///________\///__\///////////////__
"""

STARTUP_TITLE = _STARTUP_TITLE.replace("_", style("_", fg="bright_green")) \
    .replace("/", style("/", fg="bright_blue", bold=True)) \
    .replace("\\", style("\\", fg="bright_blue", bold=True))


machine_info = f"{platform.system()} v:{platform.version()}, {(platform.machine(), platform.architecture()[0])}"
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
qautolinguist_version = qal_version
python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"


white_bold_style = click.style("[*] ", fg="white", bold=True, reset=False)
blue_style = click.style(" => ", fg="blue")
black_underlined_style = style(" ", fg="bright_yellow", bold=True, underline=True, reset=False)

STARTUP_DESC = (
    f"{white_bold_style}Running on:{blue_style}{black_underlined_style}{machine_info}\n"
    f"{white_bold_style}Time:{blue_style}{black_underlined_style}{current_time}\n"
    f"{white_bold_style}QAutoLinguist version:{blue_style}{black_underlined_style}{qautolinguist_version}\n"
    f"{white_bold_style}Python version:{blue_style}{black_underlined_style}{python_version}\n"
    f"{white_bold_style}Welcome to QAutoLinguist Command Interface\n"
    f"{white_bold_style}QAL aim is to automate the internationalization of Qt (.ts) projects with machine translation.\n"
    "\n"
    f"{white_bold_style}Type >>> qautolinguist [--help] to get more in-depth information about available commands.\n"
    f"{white_bold_style}See https://backest-lad.gitbook.io/qautolinguist/ to get further information."
    "\n"
)






# colors = {
#     "Q": "bright_yellow",
#     "A": "bright_white",
#     "L": "bright_green",
#     "rest": "black"
# }

# def colorize_ascii_startup(ascii_text: List[str] = STARTUP_TITLE.strip().splitlines()) -> List[str]:
    
#     ytes = []
    
#     for row in ascii_text:
        
#         q_start = row.find("/")
#         if q_start == -1:
#             q_start = row.find("\\")
            
#         q_final =  row[q_start:].find("_")+q_start
#         q = style(row[q_start:q_final], fg=colors.get("Q", "bright_yellow"), bold=True)

#         a_start = row[q_final:].find("/") + q_final
#         if a_start == -1:
#             a_start = row[q_final:].find("\\") + q_final
#         a_final = row[a_start:].find("_") + a_start
#         a = style(row[a_start:a_final], fg=colors.get("A", "bright_white"), bold=True) 

#         l_start = row[a_final:].find("/") + a_final
#         if l_start == -1:
#             l_start = row[a_final:].find("\\") + a_final
#         l_final = row[l_start:].find("_")+ l_start
#         l = style(row[l_start:l_final], fg=colors.get("L", "bright_green"), bold=True) 

#         styled_row: str = style(row[:q_start], fg=colors.get("rest", "bright_black"), bold=True) + q \
#             + style(row[q_final:a_start], fg=colors.get("rest", "bright_black"), bold=True) + a \
#             + style(row[a_final:l_start], fg=colors.get("rest", "bright_black"), bold=True) + l \
#             + style(row[l_final:], fg=colors.get("rest", "bright_black"), bold=True)
            
#         ytes.append(styled_row)
    
#     return ytes

# echo("\n".join(colorize_ascii_startup()))


def startup_page():
    # clear()
    system("cls") if name == "nt" else system("clear")
    echo(STARTUP_TITLE)
    echo(STARTUP_DESC)
    
    

startup_page()