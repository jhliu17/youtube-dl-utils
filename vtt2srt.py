import srt
import os


# 这个脚本的作用是
# 将油管的双行 vtt 字幕转成 srt 字幕后，再转成单行
# 因为油管的字幕总是会有重复的 0.1 秒的字幕，将 ffmpeg 转成的 srt 字幕导入到 arctime 里
# 会在每一行都有重复


def vtt_to_srt(输入文件):
    输入文件 = 输入文件.strip('"')
    输出文件 = os.path.splitext(输入文件)[0] + '.srt'

    if os.path.exists(输出文件):
        print(f'{输出文件} already exist')
        return

    command = f'ffmpeg -y -i "{输入文件}" "{输出文件}"'
    print(f'command: {command}')
    state = os.system(command)

    if state != 0:
        raise RuntimeError(f'Fail to convert vtt file {输入文件}')

    try:
        with open(输出文件, 'r', encoding='utf-8') as f:
            输入文件内容 = f.read()
    except:
        with open(输出文件, 'r', encoding='gbk') as f:
            输入文件内容 = f.read()

    输入字幕列表 = list(srt.parse(输入文件内容))
    输出字幕列表 = []

    for _, subtitle in enumerate(输入字幕列表):
        if subtitle.end.seconds == subtitle.start.seconds and subtitle.end.microseconds - subtitle.start.microseconds == 10000:
            continue
        subtitle.content = subtitle.content.split('\n')[1]
        输出字幕列表.append(subtitle)

    输出文件内容 = srt.compose(输出字幕列表, reindex=True, start_index=1, strict=True)
    with open(输出文件, 'w', encoding='utf-8') as out:
        out.write(输出文件内容)


if __name__ == "__main__":

    for root, dirs, files in os.walk('video'):
        for name in files:
            if name.endswith('.vtt'):
                vtt_to_srt(os.path.join(root, name))

    print('\n\n\n')
    print('完成')
