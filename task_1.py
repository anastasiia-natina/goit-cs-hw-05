import argparse
import asyncio
import logging
from aiopath import AsyncPath
import shutil


async def copy_file(source_file: AsyncPath, destination_file: AsyncPath) -> None:
    
    try:
        await destination_file.parent.mkdir(parents=True, exist_ok=True)
        await asyncio.to_thread(shutil.copy, source_file, destination_file)
        logging.info(f"Скопійовано файл {source_file.name} до {destination_file}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні файлу {source_file.name}: {e}")


async def read_folder(source_folder: AsyncPath, output_folder: AsyncPath) -> None:
    
    async for entry in source_folder.iterdir():
        if await entry.is_dir():
            await read_folder(entry, output_folder)
        else:
            destination_subfolder = output_folder / entry.suffix.lstrip('.')
            await copy_file(entry, destination_subfolder / entry.name)


async def main() -> None:

    parser = argparse.ArgumentParser()
    parser.add_argument("source_folder", help="Шлях до вихідної папки")
    parser.add_argument("output_folder", help="Шлях до цільової папки")
    args = parser.parse_args()

    source_folder = AsyncPath(args.source_folder)
    output_folder = AsyncPath(args.output_folder)

    if not await source_folder.exists():
        logging.error(f"Вихідна папка {source_folder} не існує.")
        exit(1)

    logging.info(f"Початок сортування файлів з {source_folder} до {output_folder}")
    try:
        await read_folder(source_folder, output_folder)
    except KeyboardInterrupt:
        logging.info("Переривання...")
    finally:
        logging.info("Сортування файлів завершено.")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    asyncio.run(main())