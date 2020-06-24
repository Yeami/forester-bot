from mutagen.mp3 import MP3


def convert(seconds):
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return hours, minutes, seconds


def format_time(time):
    return time if time else '00'


def get_audio_length(audio):
    hours, minutes, seconds = convert(int(MP3(audio).info.length))

    return f'{format_time(hours)}:{format_time(minutes)}:{format_time(seconds)}'
