
import math

def jdFromDate(dd, mm, yy):
    a = int((14 - mm) / 12)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + int((153 * m + 2) / 5) + 365 * y
    jd += int(y / 4) - int(y / 100) + int(y / 400) - 32045
    return jd

def jdToDate(jd):
    a = jd + 32044
    b = int((4 * a + 3) / 146097)
    c = a - int((b * 146097) / 4)
    d = int((4 * c + 3) / 1461)
    e = c - int((1461 * d) / 4)
    m = int((5 * e + 2) / 153)
    day = e - int((153 * m + 2) / 5) + 1
    month = m + 3 - 12 * int(m / 10)
    year = b * 100 + d - 4800 + int(m / 10)
    return (day, month, year)

def getNewMoonDay(k, timeZone):
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = math.pi / 180
    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * dr * M)
    C1 -= 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(dr * 2 * Mpr)
    C1 -= 0.0004 * math.sin(dr * 3 * Mpr)
    C1 += 0.0104 * math.sin(dr * 2 * F) - 0.0051 * math.sin(dr * (M + Mpr))
    C1 -= 0.0074 * math.sin(dr * (M - Mpr)) + 0.0004 * math.sin(dr * (2 * F + M))
    C1 -= 0.0004 * math.sin(dr * (2 * F - M)) - 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 += 0.0010 * math.sin(dr * (2 * F - Mpr)) + 0.0005 * math.sin(dr * (2 * Mpr + M))
    if T < -11:
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2
    JdNew = Jd1 + C1 - deltat
    return int(JdNew + 0.5 + timeZone / 24)

def getSunLongitude(jdn, timeZone):
    T = (jdn - 2451545.5 - timeZone / 24) / 36525
    T2 = T * T
    dr = math.pi / 180
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL += (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = L0 + DL
    L *= dr
    L = L - math.pi * 2 * (int(L / (math.pi * 2)))
    return int(L / math.pi * 6)

def getLunarMonth11(yy, timeZone):
    off = jdFromDate(31, 12, yy) - 2415021
    k = int(off / 29.530588853)
    nm = getNewMoonDay(k, timeZone)
    sunLong = getSunLongitude(nm, timeZone)
    if sunLong >= 9:
        nm = getNewMoonDay(k - 1, timeZone)
    return nm

def getLeapMonthOffset(a11, timeZone):
    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    last = 0
    i = 1
    arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone)
    while True:
        last = arc
        i += 1
        arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone)
        if arc == last or i >= 14:
            break
    return i - 1

def convertSolar2Lunar(dd, mm, yy, timeZone):
    dayNumber = jdFromDate(dd, mm, yy)
    k = int((dayNumber - 2415021.076998695) / 29.530588853)
    monthStart = getNewMoonDay(k + 1, timeZone)
    if monthStart > dayNumber:
        monthStart = getNewMoonDay(k, timeZone)
    a11 = getLunarMonth11(yy, timeZone)
    b11 = a11
    if a11 >= monthStart:
        lunarYear = yy
        a11 = getLunarMonth11(yy - 1, timeZone)
    else:
        lunarYear = yy + 1
        b11 = getLunarMonth11(yy + 1, timeZone)
    lunarDay = dayNumber - monthStart + 1
    diff = int((monthStart - a11) / 29)
    lunarLeap = 0
    lunarMonth = diff + 11
    if b11 - a11 > 365:
        leapMonthDiff = getLeapMonthOffset(a11, timeZone)
        if diff >= leapMonthDiff:
            lunarMonth = diff + 10
            if diff == leapMonthDiff:
                lunarLeap = 1
    if lunarMonth > 12:
        lunarMonth = lunarMonth - 12
    if lunarMonth >= 11 and diff < 4:
        lunarYear -= 1
    return (int(lunarDay), int(lunarMonth), int(lunarYear))
