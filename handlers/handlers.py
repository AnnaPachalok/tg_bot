from aiogram import types 
from aiogram.filters import CommandStart, Command
from aiogram import Router, types, F
from random import choice
from kbrds.reply import help_kb
from storage.data import InfoState
from aiogram.fsm.context import FSMContext

private_router = Router()

@private_router.message(CommandStart())#команда/
async def command_start(message: types.Message):
    await message.answer(
        "Привіт,я купібара бот,та можу допогти тобі за допомогою своїх команд",
        reply_markup=help_kb.as_markup(resize_keyboard=True)
        )

@private_router.message(Command("help"))
async def command_help(message: types.Message):
    await message.answer("""
    /start - початок роботи
    /help - допомога
    інфо - показує інфо про тебе
    анекдот - розказує анекдот                                                                        
    """)

@private_router.message(F.text == "інфо")
async def info(message: types.Message):
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username
    user_id = message.from_user.id

    await message.answer(f"""
Твоє ім'я - {first_name}
Твоє прізвище - {last_name}
Твій -{username}
Твій - {user_id}
""")


@private_router.message(F.text == "анекдот")
async def anekdot(message: types.Message):
    anekdots_list = [
    "— Сину, ти чому щоденник сховав?\n— Він у розшуку, мамо.",
    "— Чому ви спізнились на роботу?\n— Не хотів перевтомитися на початку тижня.",
    "Йде їжачок лісом, несе кактус. Назустріч йому ведмідь:\n— Їжачок, що це в тебе?\n— Мій син, після стрижки.",
    "— Лікарю, коли я п’ю каву, у мене болить око.\n— А ви ложечку з чашки виймайте.",
    "Школа життя — єдина, де спочатку дають іспит, а вже потім — урок.",
    "Дівчина каже хлопцю:\n— Я тебе кохаю!\nХлопець:\n— Дякую, я стараюся.",
    "У бібліотеці:\n— Де можна знайти книжку «Чоловік — господар у домі»?\n— Фантастика — третя полиця зліва.",
    "— У вас чудове резюме, чому ви пішли з попередньої роботи?\n— Втекла совість...",
    "— Як правильно: «наші люди в булочну на таксі не їздять» чи «їдуть»?\n— Правильно: пішки йдуть.",
    "— Куме, ви чого сьогодні без шапки?\n— Та думаю: або голова болітиме, або шапка загубиться. Хай уже голова болить."
    ]
    random_anekdot = choice(anekdots_list)
    await message.answer(random_anekdot)

@private_router.message(F.text == "заповнити анкету")
async def fill_age(message: types.Message, state: FSMContext):
    await message.answer("Сільки тобі років?")
    await state.set_state(InfoState.age)

@private_router.message(InfoState.age)
async def fill_gender(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer("{Хлопець|Дівчина}")
    await state.set_state(InfoState.gender)

@private_router.message(InfoState.gender)
async def fill_city(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text)
    await message.answer("З якого ти міста?")
    await state.set_state(InfoState.city)

@private_router.message(InfoState.city)
async def fill_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Залиш свій номер телефону")
    await state.set_state(InfoState.phone_number)

@private_router.message(InfoState.phone_number)
async def fill_birthday(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await message.answer("Введи свою дату народження")
    await state.set_state(InfoState.birthday)

@private_router.message(InfoState.birthday)
async def fill_birthday(message: types.Message, state: FSMContext):
    await state.update_data(birthday=message.text)
    data = await state.get_data()
    print(data)
    await message.answer(f"""
Дякую за заповнення анкети
Вік: {data["age"]}
Стать:{data["gender"]}                    
Місто:{data["city"]}                    
Номер телефону:{data["phone_number"]}                     
День народження:{data["birthday"]}                     
""")

    await state.clear()

