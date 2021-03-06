## Telegram bot for house chores for children

This bot was born because [RoosterMoney](https://roostermoney.com/) decided they're going to offer the app only customers based on UK. My kid wanted to save for a new bass so the app was a brilliant way to add chores worth of some money she could do and save.

The app uses Telegram API and YNAB API in a way my daughter is able to select a chore she has done simply by typing a Telegram command. Then the amount would be added to her savings budget accordingly.

**Please note:** This bot is for personal use. It might not work for you and it has direct strings translated to Finnish language.

<img src="https://user-images.githubusercontent.com/1534150/168444711-3146d91b-6acf-475e-a308-2a627acf5ba8.jpg" width="320" />

### Requirements 

* Python 3.8
* pipenv
* Linux/WSL
* [Python YNAB API](https://github.com/dmlerner/ynab-api)
* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)

### Installation

1. Create your bot via [BotFather](https://t.me/botfather)
2. Set up at least with `/newbot`, `/setdescription`, `/setname` and `/setuserpic`.
3. Set up command options with `/setcommands`:

```
ohje - Näytä ohje.
kotihommat - Lisää tehty kotityö, näytä valinnat.
peru - Peru/piilota valinnat.
saldo - Näytä paljonko tällä hetkellä on kertynyt säästöjä.
poista - Poista haluttu summa, esim. /poista 0.50
```

4. Disable privacy mode with `/setprivacy`, if this is not set the bot cannot reply to a channel
5. Rename .env-example to .env
6. Add your personal bot `TOKEN` to .env file
7. Run `pipenv install -r requirements.txt` (sudo might be needef or WSL)
8. Add [YNAB API](https://api.youneedabudget.com/) credentials to .env (you can get your budget ID from address bar when going to [app.youneedabudget.com](https://app.youneedabudget.com/)):
9. Run `pipenv run python bot.py`

### Features

* Add chores via command/bubbles
* Update balance directly to YNAB budget
* Get current savings amount from YNAB
* List chore selection and amounts
* Remove amounts directly from YNAB budget (if accidental taps or some money is used)

### Resources that helped me

* [How to create a Telegram Bot in Python in under 10 minutes](https://www.codementor.io/@karandeepbatra/part-1-how-to-create-a-telegram-bot-in-python-in-under-10-minutes-19yfdv4wrq)
* [Making a Telegram bot using Python](https://pythonprogramming.org/making-a-telegram-bot-using-python/)
