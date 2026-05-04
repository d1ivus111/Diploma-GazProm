import asyncio
import zipfile
import time
import os
import sys
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from ollama import chat
from datasets import load_dataset

# ========== Конфигурация ==========
BOT_TOKEN = os.getenv("BOT_TOKEN", "8747047863:AAEtbIqoOfDxTVxxyueIICApJU4J65DAsPg")  # лучше через переменную окружения
OLLAMA_MODEL = "deepseek-r1:8b"  # модель, которую загрузили в ollama
DATASET_NAME = "imdb"  # датасет из Hugging Face (для примера)

# Загружаем датасет один раз при старте (кэшируется HF)
try:
    dataset = load_dataset(DATASET_NAME, split="train")
    print(f"Датасет {DATASET_NAME} загружен, {len(dataset)} записей")
except Exception as e:
    print(f"Не удалось загрузить датасет: {e}")
    dataset = None


async def execute_command(cmd: str, update: Update, timeout: int = 300) -> str:
    """Выполняет shell-команду с таймаутом"""
    try:
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout)
        output = (f"STDOUT:\n{stdout.decode().strip()}" if stdout else "")
        output += f"\nSTDERR:\n{stderr.decode().strip()}" if stderr else ""
        return output.strip()
    except asyncio.TimeoutError:
        return f"❌ Таймаут ({timeout} сек)"
    except Exception as e:
        return f"⚠️ Ошибка: {str(e)}"


async def query_ollama(prompt: str) -> str:
    """
    Отправляет запрос в Ollama (асинхронная обёртка над синхронным вызовом).
    Запускаем синхронный `ollama.chat` в отдельном потоке, чтобы не блокировать event loop.
    """
    try:
        response = await asyncio.to_thread(
            chat,
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.message.content
    except Exception as e:
        return f"Ошибка Ollama: {str(e)}. Запущен ли сервер? Проверь http://localhost:11434"


async def run_all_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск тестов и сохранение результатов"""
    await update.message.reply_text("🔍 Запускаю тесты...")

    # Подготовка директории для результатов
    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск pytest
    result = await execute_command(
        "pytest -s -v test/ --alluredir=./results",
        update
    )

    # Проверка наличия результатов тестов
    # if not any(results_dir.iterdir()):
    #     await update.message.reply_text("⚠️ Внимание: allure-results пуст. Возможно, тесты не запустились.")
    #     return

    # Отправка сокращенного отчета
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
    )


async def run_ui_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск тестов и сохранение результатов"""
    await update.message.reply_text("🔍 Запускаю тесты...")

    # Подготовка директории для результатов
    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск pytest
    result = await execute_command(
        "pytest -s -v test/ui/ --alluredir=./results",
        update
    )

    # Проверка наличия результатов тестов
    # if not any(results_dir.iterdir()):
    #     await update.message.reply_text("⚠️ Внимание: allure-results пуст. Возможно, тесты не запустились.")
    #     return

    # Отправка сокращенного отчета
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
    )


async def run_api_tests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск тестов и сохранение результатов"""
    await update.message.reply_text("🔍 Запускаю тесты...")

    # Подготовка директории для результатов
    results_dir = Path("./results")
    results_dir.mkdir(exist_ok=True)

    # Очистка предыдущих результатов
    for file in results_dir.glob("*"):
        file.unlink()

    # Запуск pytest
    result = await execute_command(
        "pytest -s -v test/api/ --alluredir=./results",
        update
    )

    # Проверка наличия результатов тестов
    # if not any(results_dir.iterdir()):
    #     await update.message.reply_text("⚠️ Внимание: allure-results пуст. Возможно, тесты не запустились.")
    #     return

    # Отправка сокращенного отчета
    short_result = "\n".join([line for line in result.split("\n") if "FAILED" in line or "ERROR" in line])
    await update.message.reply_text(
        f"📊 Результаты тестов:\n{short_result[:3000]}" if short_result else "✅ Все тесты прошли успешно!"
    )


async def generate_allure_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Генерация отчета и отправка архива"""
    try:
        # Проверка наличия результатов тестов
        results_dir = Path("./results")
        if not results_dir.exists() or not any(results_dir.iterdir()):
            await update.message.reply_text("❌ Нет данных для отчета: папка allure-results пуста или отсутствует")
            return

        # Генерация отчета
        await update.message.reply_text("📈 Генерирую Allure-отчет...")
        report_dir = Path("./allure-report")
        report_dir.mkdir(exist_ok=True)

        gen_result = await execute_command(
            "allure generate ./results --clean -o ./allure-report",
            update
        )

        # Проверка наличия сгенерированного отчета
        report_index = report_dir / "index.html"
        if not report_index.exists():
            await update.message.reply_text("❌ Ошибка генерации: index.html не найден в allure-report")
            return

        # Создание архива
        await update.message.reply_text("📦 Создаю архив...")
        timestamp = int(time.time())
        zip_name = f"allure_report_{timestamp}.zip"

        with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Добавляем allure-report
            for root, _, files in os.walk(report_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.join("allure-report", os.path.relpath(file_path, report_dir))
                    zipf.write(file_path, arcname=arcname)

            # Добавляем allure-results
            for root, _, files in os.walk(results_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = os.path.join("./results", os.path.relpath(file_path, results_dir))
                    zipf.write(file_path, arcname=arcname)

        # Отправка архива
        await update.message.reply_text("📤 Отправляю архив...")
        with open(zip_name, 'rb') as zip_file:
            await context.bot.send_document(
                chat_id=update.effective_chat.id,
                document=zip_file,
                filename=zip_name,
                caption="📊 Allure Report (включая исходные данные)"
            )

        # Очистка временных файлов
        os.remove(zip_name)
        await update.message.reply_text("✅ Отчет успешно отправлен!")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Критическая ошибка: {str(e)}")


async def full_cycle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Полный цикл: тесты + отчет"""
    await run_all_tests(update, context)
    await generate_allure_report(update, context)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('''
Нажми МЕНЮ ↙️, чтобы выбрать команду, которую выполнит бот.
👋Информация обо мне
🧠Запустить API тест
🖼Запустить UI тест
🔍Запустить все тесты
🧠Воспользоваться ИИ ( /ask {вопрос} )
    ''')


async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about_text = '👋Привет!\nМеня зовут Дарья. Мне 18 лет, и я студентка IT - Шаг академии.'

    await update.message.reply_text(about_text)


async def pwd_env(update: Update, context: ContextTypes.DEFAULT_TYPE):
    venv_path = sys.prefix
    venv_env = os.environ.get("VIRTUAL_ENV")
    if venv_env:
        results = f"Активно виртуальное окружение: {venv_env}"
    else:
        results = f"Используется Python из: {venv_path}"

    await update.message.reply_text(f"Какое окружение используется: {results}")


async def deactivate_to_venv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Запуск тестов и сохранение результатов"""
    await update.message.reply_text("Выхожу из venv окружения")
    await execute_command("deactivate", update)
    await update.message.reply_text("Выход из venv окружения успешен")


# === НОВЫЕ КОМАНДЫ ===

async def ask_neural(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Отправляет запрос нейросети через Ollama.
    Использование: /ask Как дела?
    """
    user_message = " ".join(context.args) if context.args else None
    if not user_message:
        await update.message.reply_text(
            "Пожалуйста, напишите вопрос после команды, например:\n/ask Привет, как тебя зовут?")
        return

    await update.message.reply_text("🤔 Думаю...")
    answer = await query_ollama(user_message)
    # Telegram ограничивает длину сообщения 4096 символами
    safe_answer = answer[:4000] + "..." if len(answer) > 4000 else answer
    await update.message.reply_text(safe_answer)


async def show_random_dataset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Показывает случайную запись из загруженного датасета (IMDb)"""
    if dataset is None:
        await update.message.reply_text(
            "❌ Датасет не загружен. Проверьте подключение к Hugging Face или название датасета.")
        return

    # случайный индекс
    import random
    idx = random.randint(0, len(dataset) - 1)
    record = dataset[idx]
    text = record["text"][:500]  # у датасета IMDb есть поля "text" и "label"
    label = record["label"]
    sentiment = "положительный" if label == 1 else "отрицательный"
    await update.message.reply_text(
        f"🎲 Случайный отзыв из IMDb:\n\n{text}...\n\nТональность: {sentiment}"
    )


async def search_dataset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Поиск по датасету (простой фильтр).
    Использование: /search_data слово
    """
    if dataset is None:
        await update.message.reply_text("❌ Датасет недоступен.")
        return
    query = " ".join(context.args).lower() if context.args else None
    if not query:
        await update.message.reply_text("Укажите поисковый запрос, например: /search_data amazing")
        return

    # ищем первые 3 записи, содержащие запрос в поле text (медленно для больших датасетов, но для демо ок)
    results = []
    for i, record in enumerate(dataset):
        if query in record["text"].lower():
            results.append((record["text"][:200], record["label"]))
            if len(results) >= 3:
                break
    if not results:
        await update.message.reply_text(f"По запросу '{query}' ничего не найдено.")
        return

    reply = f"🔍 Результаты поиска по '{query}':\n\n"
    for text_snip, label in results:
        sentiment = "👍" if label == 1 else "👎"
        reply += f"{sentiment} {text_snip}...\n\n"
    await update.message.reply_text(reply[:4000])


# ========== main ==========
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # все команды
    handlers = [
        CommandHandler("start", start),
        CommandHandler("about", about),
        CommandHandler("run_all_tests", run_all_tests),
        CommandHandler("run_ui_tests", run_ui_tests),
        CommandHandler("run_api_tests", run_api_tests),
        CommandHandler("allurereport", generate_allure_report),
        CommandHandler("fullreport", full_cycle),
        CommandHandler("ask", ask_neural),
        CommandHandler("dataset", show_random_dataset),
        CommandHandler("search_data", search_dataset),
    ]

    for handler in handlers:
        application.add_handler(handler)

    application.run_polling()


if __name__ == "__main__":
    main()
