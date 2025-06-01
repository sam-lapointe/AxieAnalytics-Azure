import json
import asyncio
from axies import Axie

axie_levels = {
    '1': {'total_xp': 0, 'level_up_xp': 100},
    '2': {'total_xp': 100, 'level_up_xp': 210},
    '3': {'total_xp': 310, 'level_up_xp': 430},
    '4': {'total_xp': 740, 'level_up_xp': 740},
    '5': {'total_xp': 1480, 'level_up_xp': 1140},
    '6': {'total_xp': 2620, 'level_up_xp': 1640},
    '7': {'total_xp': 4260, 'level_up_xp': 2260},
    '8': {'total_xp': 6520, 'level_up_xp': 2980},
    '9': {'total_xp': 9500, 'level_up_xp': 3810},
    '10': {'total_xp': 13310, 'level_up_xp': 4760},
    '11': {'total_xp': 18070, 'level_up_xp': 5830},
    '12': {'total_xp': 23900, 'level_up_xp': 7010},
    '13': {'total_xp': 30910, 'level_up_xp': 8320},
    '14': {'total_xp': 39230, 'level_up_xp': 9760},
    '15': {'total_xp': 48990, 'level_up_xp': 11310},
    '16': {'total_xp': 60300, 'level_up_xp': 13010},
    '17': {'total_xp': 73310, 'level_up_xp': 14830},
    '18': {'total_xp': 88140, 'level_up_xp': 16780},
    '19': {'total_xp': 104920, 'level_up_xp': 18870},
    '20': {'total_xp': 123790, 'level_up_xp': 21090},
    '21': {'total_xp': 144880, 'level_up_xp': 23460},
    '22': {'total_xp': 168340, 'level_up_xp': 25950},
    '23': {'total_xp': 194290, 'level_up_xp': 28600},
    '24': {'total_xp': 222890, 'level_up_xp': 31380},
    '25': {'total_xp': 254270, 'level_up_xp': 34300},
    '26': {'total_xp': 288570, 'level_up_xp': 37380},
    '27': {'total_xp': 325950, 'level_up_xp': 40590},
    '28': {'total_xp': 366540, 'level_up_xp': 43950},
    '29': {'total_xp': 410490, 'level_up_xp': 47470},
    '30': {'total_xp': 457960, 'level_up_xp': 51130},
    '31': {'total_xp': 509090, 'level_up_xp': 54940},
    '32': {'total_xp': 564030, 'level_up_xp': 58910},
    '33': {'total_xp': 622940, 'level_up_xp': 63020},
    '34': {'total_xp': 685960, 'level_up_xp': 67300},
    '35': {'total_xp': 753260, 'level_up_xp': 71720},
    '36': {'total_xp': 824980, 'level_up_xp': 76300},
    '37': {'total_xp': 901280, 'level_up_xp': 81040},
    '38': {'total_xp': 982320, 'level_up_xp': 85940},
    '39': {'total_xp': 1068260, 'level_up_xp': 91000},
    '40': {'total_xp': 1159260, 'level_up_xp': 96210},
    '41': {'total_xp': 1255470, 'level_up_xp': 101590},
    '42': {'total_xp': 1357060, 'level_up_xp': 107130},
    '43': {'total_xp': 1464190, 'level_up_xp': 112820},
    '44': {'total_xp': 1577010, 'level_up_xp': 118700},
    '45': {'total_xp': 1695710, 'level_up_xp': 124720},
    '46': {'total_xp': 1820430, 'level_up_xp': 130920},
    '47': {'total_xp': 1951350, 'level_up_xp': 137280},
    '48': {'total_xp': 2088630, 'level_up_xp': 143800},
    '49': {'total_xp': 2232430, 'level_up_xp': 150500},
    '50': {'total_xp': 2382930, 'level_up_xp': 157370},
    '51': {'total_xp': 2540300, 'level_up_xp': 164390},
    '52': {'total_xp': 2704690, 'level_up_xp': 171600},
    '53': {'total_xp': 2876290, 'level_up_xp': 178970},
    '54': {'total_xp': 3055260, 'level_up_xp': 186520},
    '55': {'total_xp': 3241780, 'level_up_xp': 194240},
    '56': {'total_xp': 3436020, 'level_up_xp': 202120},
    '57': {'total_xp': 3638140, 'level_up_xp': 210190},
    '58': {'total_xp': 3848330, 'level_up_xp': 218430},
    '59': {'total_xp': 4066760, 'level_up_xp': 226840},
    '60': {'total_xp': 4293600, 'level_up_xp': 235430}
}

async def main():
    # 1653 Good test
    axie_data, axie_activities = await Axie("yS3sQSVozLtALtkCgpGYUu0aBEnxE519", 3517, 1746226281).process_axie_data()
    print(axie_data)
    print(axie_activities)



if __name__ == "__main__":
    asyncio.run(main())