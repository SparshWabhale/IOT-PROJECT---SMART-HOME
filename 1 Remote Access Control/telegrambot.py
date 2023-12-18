import sys
import time
import random
import datetime
import telepot
import RPi.GPIO as GPIO


def on(pin):  # Switch on function - turns GPIO pin in pi to HIGH
    GPIO.output(pin, GPIO.HIGH)
    return


def off(pin):  # Switch off function - turns GPIO pin in pi to LOW
    GPIO.output(pin, GPIO.LOW)
    return


GPIO.setmode(GPIO.BOARD)
GPIO.setup(2, GPIO.OUT)  # GPIO pin no. to which led is connected


def handle(msg):
    chat_id = msg["chat"]["id"]  # takes chat and id from the json sent to telegrambot
    command = msg[
        "text"
    ]  # assigning value for command from the msg sent to the bot in telegram

    print("Got command: %s", command)

    if command == "on":
        bot.sendMessage(chat_id, on(2))
    elif command == "off":
        bot.sendMessage(chat_id, off(2))


bot = telepot.Bot(
    "6015942571:AAGY9Fjm3tofyeUxjvcwbLI4PCcu1TSB7O4"
)  # bot ID to enable privacy, only people with this ID can know the bot.
bot.message_loop(handle)
print("I am listening...")

while 1:
    time.sleep(10)
