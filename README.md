# Mirrors V1.0.0

> 𝗠𝗶𝗿𝗿𝗼𝗿𝘀 — программа для загрузки медиа по ссылке.

![Made with love](https://img.shields.io/badge/made%20with-%E2%9D%A4-red.svg) ![GitHub stars](https://img.shields.io/github/stars/justiceDev1/Mirrors.svg?style=social)
![Mirrors](https://i.postimg.cc/zXzH1M7K/Snimok-ekrana-2026-11-16-154010.png)



𝗠𝗶𝗿𝗿𝗼𝗿𝘀 — небольшая консольная утилита с оформленным интерфейсом на базе Rich. Она позволяет скачивать видео, аудио и превью по ссылкам, показывает прогресс загрузки и выводит понятные сообщения об ошибках.

## ✨ Возможности

- скачивание видео в формате MP4
- скачивание аудио в формате MP3
- скачивание изображений по прямой ссылке
- получение превью со страниц, поддерживаемых yt-dlp
- отображение прогресса и скорости загрузки
- автоматическое создание папки MirrorsDownloads
- понятные сообщения об ошибках
- адаптация интерфейса под размер терминала

## 📦 Установка

```python
Для 𝗪𝗶𝗻𝗱𝗼𝘄𝘀 𝗖𝗠𝗗
Откройте CMD или терминал и выполните:
1) winget install --id Git.Git -e --source winget
2) winget install -e --id Python.Python.3.14 
3) git clone https://github.com/justiceDev1/Mirrors
4) cd Mirrors
5) py -m pip install -r requirements.txt
6) winget install Gyan.FFmpeg
После установки всего необходимого выполните: python3 Mirrors.py

Для 𝗟𝗶𝗻𝘂𝘅 
Откройте терминал и выполните:
1) sudo apt update
2) sudo apt install python3 python3-pip ffmpeg git
3) git clone https://github.com/justiceDev1/Mirrors
4) cd Mirrors
5) python3 -m pip install -r requirements.txt
После установки всего необходимого выполните: python3 Mirrors.py

Для Termux
Откройте Termux и выполните:
1) pkg update
2) pkg install python ffmpeg
3) pkg install git
4) git clone https://github.com/justiceDev1/Mirrors
5) cd Mirrors
6) pip install -r requirements.txt
После установки всего необходимого выполните: python3 Mirrors.py
```

## 🚀 Использование

```python
После запуска программы выберите действия:
[1] Скачать видео
[2] Скачать аудио
[3] Скачать фото/превью
[0] Выйти из программы
```

## 👤 Автор

**justiceDev1** — [@justiceDev1](https://github.com/justiceDev1)

