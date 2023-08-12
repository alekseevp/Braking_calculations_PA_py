import pandas as pd


def calculate_intervals(Vn, i, Q, P, u, thetachr, thetakr, a, c, A, B, C):
    # Функции для расчета средней скорости на интервале
    def calculate_Vcp(Vn, Vk):
        return (Vn + Vk) / 2

    def calculate_tp(Vcp):
        return a - ((c * i) / calculate_bt(Vcp))

    def calculate_dt(Vcp, dSd):
        return (3.6 * dSd) / Vcp

    def calculate_dSp(Vn, Vk):
        Vcp = calculate_Vcp(Vn, Vk)
        tp = calculate_tp(Vcp)
        return 0.278 * Vn * tp

    def calculate_zero_interval(Vn, Vk):
        Vcp = calculate_Vcp(Vn, Vk)
        tp = calculate_tp(Vcp)
        dS = calculate_dSp(Vn, Vk)
        dΣS = dS
        dΣt = tp
        return Vcp, tp, dS, dΣS, dΣt

    def calculate_next_interval(Vn, Vk, Vcp_prev, dΣS_prev, dΣt_prev):
        Vcp = calculate_Vcp(Vn, Vk)
        dSd = calculate_dSd(Vn, Vk)
        tp = calculate_dt(Vcp, dSd)
        dS = dSd
        dΣS = dΣS_prev + dS
        dΣt = dΣt_prev + tp
        return Vcp, tp, dS, dΣS, dΣt

    def calculate_Fkkr(Vcp):
        return 0.36 * ((Vcp + 150) / (2 * Vcp + 150))

    def calculate_Fchkr(Vcp):
        return 0.27 * ((Vcp + 100) / (5 * Vcp + 100))

    def calculate_bkt(Vcp, thetakr):
        return 1000 * thetakr * calculate_Fkkr(Vcp)

    def calculate_bcht(Vcp, thetachr):
        return 1000 * thetachr * calculate_Fchkr(Vcp)

    def calculate_bt(Vcp):
        return calculate_bkt(Vcp, thetakr) + calculate_bcht(Vcp, thetachr)

    def calculate_wox(Vcp):
        return 2.4 + 0.011 * Vcp + 0.00035 * Vcp**2

    def calculate_wo(Vcp):
        return A + B * Vcp + C * Vcp**2

    def calculate_w(Vcp):
        return (calculate_wo(Vcp) * Q + calculate_wox(Vcp) * P) / (P + Q)

    def calculate_dSd(Vn, Vk):
        Vcp = calculate_Vcp(Vn, Vk)
        return (500 * (Vn**2 - Vk**2)) / (u * (calculate_bt(Vcp) + i + calculate_w(Vcp)))

    intervals_data = []
    Vk = Vn

    # Расчет для нулевого интервала
    Vcp, tp, dS, dΣS, dΣt = calculate_zero_interval(Vn, Vk)

    intervals_data.append({
        "Номер интервала": len(intervals_data) + 1,
        "Vн": Vn,
        "Vк": Vk,
        "Vср": Vcp,
        "Фчкр": calculate_Fchkr(Vcp),
        "bчт": calculate_bcht(Vcp, thetachr),
        "Фккр": calculate_Fkkr(Vcp),
        "bкт": calculate_bkt(Vcp, thetakr),
        "bт": calculate_bt(Vcp),
        "wo": calculate_wo(Vcp),
        "wox": calculate_wox(Vcp),
        "w": calculate_w(Vcp),
        "dS": dS,
        "dΣS": dΣS,
        "dt": tp,
        "dΣt": dΣt,
    })

    # Расчет для первого интервала, если начальная скорость не krатна 10
    if Vn % 10 != 0:
        Vk = Vn - (Vn % 10)
    else:
        Vk = Vn - 10

    while Vk >= 0:
        Vcp, tp, dS, dΣS, dΣt = calculate_next_interval(Vn, Vk, Vcp, dΣS, dΣt)

        intervals_data.append({
            "Номер интервала": len(intervals_data) + 1,
            "Vн": Vn,
            "Vк": Vk,
            "Vср": Vcp,
            "Фчкр": calculate_Fchkr(Vcp),
            "bчт": calculate_bcht(Vcp, thetachr),
            "Фккр": calculate_Fkkr(Vcp),
            "bкт": calculate_bkt(Vcp, thetakr),
            "bт": calculate_bt(Vcp),
            "wo": calculate_wo(Vcp),
            "wox": calculate_wox(Vcp),
            "w": calculate_w(Vcp),
            "dS": dS,
            "dΣS": dΣS,
            "dt": tp,
            "dΣt": dΣt,
        })

        Vn = Vk
        Vk -= 10

    df = pd.DataFrame(intervals_data)
    return df


