import sys
import time
import random
import datetime
import telepot
import RPi.GPIO as GPIO


def on(pin):
    GPIO.output(pin, GPIO.HIGH)
    return


def off(pin):
    GPIO.output(pin, GPIO.LOW)
    return


GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)


def handle(msg):
    chat_id = msg["chat"]["id"]
    command = msg["text"]

    print("\n\n*****\nchat_id :%s", chat_id)
    print("Got command: %s\n*******\n\n", command)

    if command == "On_red" or command == "on_red" or command == "/on_red":
        bot.sendMessage(chat_id, on(2))
    elif command == "Off_red" or command == "off_red" or command == "/off_red":
        bot.sendMessage(chat_id, off(2))
    elif command == "On_blue" or command == "on_blue" or command == "/on_blue":
        bot.sendMessage(chat_id, on(4))
    elif command == "Off_blue" or command == "off_blue" or command == "/off_blue":
        bot.sendMessage(chat_id, off(4))
    elif command == "On_green" or command == "on_green" or command == "/on_green":
        bot.sendMessage(chat_id, on(27))
    elif command == "Off_green" or command == "off_green" or command == "/off_green":
        bot.sendMessage(chat_id, off(27))


bot = telepot.Bot("6015942571:AAGY9Fjm3tofyeUxjvcwbLI4PCcu1TSB7O4")
bot.message_loop(handle)
print("I am listening...")

while 1:
    time.sleep(10)
