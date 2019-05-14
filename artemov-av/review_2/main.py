import tg
import time

if __name__ == '__main__':
    while True:
        try:
            tg.bot.polling(none_stop=True)
        except Exception:
            time.sleep(20)
