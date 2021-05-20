#here we specify that all subsequent commands are to be run in a debian buster enviroment
FROM debian:buster-slim
#we run apt update in the enviroment specified above
RUN apt update
#we install the required packages from apt here
RUN apt install -y python3 python3-pip ffmpeg
#here we install the pip packages
RUN python3 -m pip install discord.py python-dotenv requests
#add all the discord bot files into the debian env at the location /discord-bot
COPY ./src /discord-bot
#when we run the container we cd to the discord bot foler, then run wrap.py (catch all the errors and log them)
CMD cd discord-bot;python3 wrap.py

# NOTE FOR BRANDEN
# if you wish to view the bot run
#   docker exec -it discord-bot bash
# this will open a bash shell in the discord bots container incase you wish to view it's files
# /discord-bot/logging.txt is where all errors/output go