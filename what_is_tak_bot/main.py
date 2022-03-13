import logging
import re

from aiogram import Bot, Dispatcher, executor, types

from what_is_tak_bot.config import settings

# Configure logging
logging.basicConfig(format=settings.LOG_FORMAT, level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
bot = Bot(token=settings.BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(regexp=r'что\s+такое\s+([а-яА-Я ]+)\?*')
@dp.message_handler(regexp=r'([а-яА-Я ]+)[,\s-]+что\s+это\?*')
@dp.message_handler(regexp=r'что\s+значит\s+([а-яА-Я ]+)\?*')
@dp.message_handler(regexp=r'([а-яА-Я ]+)[,\s-]+что\s+значит\?*')
@dp.message_handler(regexp=r'([а-яА-Я ]+)[,\s-]+что\s+это\s+значит\?*')
@dp.message_handler(regexp=r'([а-яА-Я ]+)[,\s-]+что\s+это\s+может\s+значить\?*')
async def what_is(message: types.Message, regexp: re.Match):
    logger.info('got %s message in what_is', message.text)
    result = await search_needle(regexp.group(1).strip())
    if result is None:
        return
    await message.answer(result, reply=settings.BOT_REPLY)


@dp.message_handler(text_contains='?')
async def question_mark(message: types.Message):
    question_words = ('как', 'что', 'сколько', 'где', 'какой', 'кто', 'когда', 'почему', 'чем', 'чего', 'куда',
                      'который', 'кому', 'зачем', 'откуда', 'чей', 'чья', 'каков', 'отчего')
    for question_word in question_words:
        if question_word in message.text:
            logger.debug('skipping %s message in question_mark', message.text)
            return
    logger.info('got %s message in question_mark', message.text)
    result = await search_needle(message.text.strip('?'))
    await message.answer(result, reply=settings.BOT_REPLY)


async def search_needle(needle: str) -> str | None:
    return f'{needle} - это так, как лучше для Вас'


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
