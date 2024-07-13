import asyncio
import argparse
import logging
import os
import shutil
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

parser = argparse.ArgumentParser()
parser.add_argument("source_folder", help="Шлях до вихідної папки")
parser.add_argument("output_folder", help="Шлях до цільової папки")
args = parser.parse_args()

source_folder = Path(args.source_folder)
output_folder = Path(args.output_folder)

if not source_folder.exists():
    logging.error(f"Вихідна папка {source_folder} не існує.")
    exit(1)

if not output_folder.exists():
    try:
        output_folder.mkdir()
    except OSError as e:
        logging.error(f"Не вдалося створити цільову папку {output_folder}: {e}")
        exit(1)

async_source_folder = os.path.join(os.path.realpath(source_folder), "")
async_output_folder = os.path.join(os.path.realpath(output_folder), "")


async def read_folder(folder):
    for entry in os.scandir(folder):
        if entry.is_dir():
            await read_folder(os.path.join(folder, entry.name))
        else:
            await copy_file(entry.name, folder)


async def copy_file(filename, folder):
    file_extension = os.path.splitext(filename)[1]
    output_subfolder = os.path.join(async_output_folder, file_extension[1:])
    
    if not os.path.exists(output_subfolder):
        try:
            os.makedirs(output_subfolder)
        except OSError as e:
            logging.error(f"Не вдалося створити підпапку {output_subfolder}: {e}")
            return

    source_file = os.path.join(folder, filename)
    destination_file = os.path.join(output_subfolder, filename)
    
    try:
        async with open(source_file, 'rb') as f_in, open(destination_file, 'wb') as f_out:
            await shutil.copyfileobj(f_in, f_out)
            logging.info(f"Скопійовано файл {filename} до {destination_file}")

    except Exception as e:
        logging.error(f"Помилка при копіюванні файлу {filename}: {e}")


async def main():
    try:
        await asyncio.gather(read_folder(async_source_folder))
    except KeyboardInterrupt:
        logging.info("Переривання...")


if __name__ == "__main__":
    logging.info(f"Початок сортування файлів з {source_folder} до {output_folder}")
    asyncio.run(main())
    logging.info("Сортування файлів завершено.")