from music21 import stream, note, chord, meter, key, tempo, instrument

# 音符轉換函數（節奏 + 八度）
def number_to_pitch_and_duration(symbol):
    base_map = {
        '1': 'Ab', '2': 'Bb', '3': 'C', '4': 'Db',
        '5': 'Eb', '6': 'F', '7': 'G'
    }

    # 取音符核心
    core = symbol.strip("-_'.")  # 如 '5_' -> '5'
    pitch_base = base_map.get(core, None)
    if pitch_base is None:
        return ('r', 1)

    # 八度
    if symbol.endswith("''"):
        octave = 6
    elif symbol.endswith("'"):
        octave = 5
    elif symbol.endswith("."):
        octave = 3
    else:
        octave = 4

    # 時值
    if '--' in symbol:
        duration = 2
    elif '_' in symbol or '-' in symbol:
        duration = 0.5
    else:
        duration = 1

    return (f"{pitch_base}{octave}", duration)

# 簡譜旋律清單（含八度與拍值）
notes = [
    '5.', '5_.', '5_.', '2', '-', '3', '2_', '1_', '1', '-', #1-2
    '1', '1_', '1_', '4', '-', '3', '2_', '1_', '2', '-', #3-4
    '2', '2_', '2_', '5', '-', '3', '2_', '1_', "6.", '-', #5-6
    "1", "7_.", "6_.", "5_.d", '1_', '2d', '1_', '1', '-', #7-8
]

# 主旋律聲部
melody = stream.Part()
melody.insert(0, instrument.Piano())
melody.append(tempo.MetronomeMark(number=90))
melody.append(meter.TimeSignature('4/4'))
melody.append(key.Key('Ab'))

# 和聲聲部
harmony = stream.Part()
harmony.insert(0, instrument.Soprano())
harmony.append(tempo.MetronomeMark(number=90))
harmony.append(meter.TimeSignature('4/4'))
harmony.append(key.Key('Ab'))

# 將音符加入旋律
for n in notes:
    pitch, dur = number_to_pitch_and_duration(n)
    if pitch == 'r':
        melody.append(note.Rest(quarterLength=dur))
    else:
        melody.append(note.Note(pitch, quarterLength=dur))

# 每小節加和弦（Ab大三和弦）
basic_chords = ['Ab3', 'C4', 'Eb4']
bars = len(notes) // 4 + 1
for _ in range(bars):
    c = chord.Chord(basic_chords)
    c.quarterLength = 4
    harmony.append(c)

# 組合並輸出
score = stream.Score()
score.insert(0, melody)
score.insert(0, harmony)

# 播放 + 匯出
#score.show('midi')                    # 播放
score.write('midi', fp='晨星快現.mid')  # 匯出 MIDI 檔
