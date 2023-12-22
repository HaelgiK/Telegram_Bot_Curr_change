# Currency Converter TelegramBot

The bot implements conversion of fiat and cryptocurrencies (USD, EUR, USDT, BTC, ETH, SOL).

When writing the bot, the pytelegrambotapi library was used.

At the first start the user is shown instructions on how to use the bot. The instructions are also available by entering the /help command

The user can use interactive buttons for conversion. Or it is possible to send a message to the bot in the form <currency name the price of which is to be found out> <currency name to be converted> <number of the first currency> with a space.

Entering the /values command displays information about all available currencies.

To take the exchange rate, the min-api.cryptocompare.com API is used and requests are sent to it using the Requests library.

The JSON library is used for parsing the received responses.

In case of a user error (e.g. an incorrect or non-existent currency is entered or a number is entered incorrectly), a written APIException exception is raised with the text explaining the error.
The error text with the error type is sent to the user in a message.

To send requests to the API, a class with a static method get_convert() is described, which takes three arguments: the name of the currency, the price of which to find out, the name of the currency, the price in which to find out, the amount of currency to be transferred and returns the desired amount in currency.

All classes are stored in the utils_1.py file.
