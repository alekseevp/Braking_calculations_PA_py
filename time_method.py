import pandas as pd



def calculate_braking_intervals(Vn, i, Q, P, u, l, thetachr, thetakr, A, B, C):
    dt = 3  # Интервал времени в секундах


    def calculate_percent(l):
        def generator_func(lst):
            for val in lst:
                yield val
            while True:
                yield 100

        if l < 500:
            thetap0 = [0, 15, 62, 87, 97, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]
            thetap500 = [0, 20, 45, 65, 80, 90, 85, 98, 100, 100, 100, 100, 100, 100, 100, 100]

            thetasost_list = [
                thetap500[i] + ((thetap0[i] - thetap500[i]) / (500 - 0)) * (500 - l)
                for i in range(len(thetap0))
            ]
        elif 500 <= l < 800:
            thetap500 = [0, 20, 45, 65, 80, 90, 85, 98, 100, 100, 100, 100, 100, 100, 100, 100]
            thetap800 = [0, 15, 35, 50, 65, 75, 85, 95, 98, 100, 100, 100, 100, 100, 100, 100]

            thetasost_list = [
                thetap800[i] + ((thetap500[i] - thetap800[i]) / (800 - 500)) * (800 - l)
                for i in range(len(thetap500))
            ]
        elif 800 <= l < 1200:
            thetap800 = [0, 15, 35, 50, 65, 75, 85, 95, 98, 100, 100, 100, 100, 100, 100, 100]
            thetap1200 = [0, 2, 20, 35, 50, 60, 70, 80, 85, 90, 94, 96, 98, 100, 100, 100]

            thetasost_list = [
                thetap1200[i] + ((thetap800[i] - thetap1200[i]) / (1200 - 800)) * (1200 - l)
                for i in range(len(thetap800))
            ]
        elif 1200 <= l < 1600:
            thetap1200 = [0, 2, 20, 35, 50, 60, 70, 80, 85, 90, 94, 96, 98, 100, 100, 100]
            thetap1600 = [0, 0, 10, 25, 35, 45, 55, 62, 70, 75, 80, 85, 90, 95, 98, 100]

            thetasost_list = [
                thetap1600[i] + ((thetap1200[i] - thetap1600[i]) / (1600 - 1200)) * (1600 - l)
                for i in range(len(thetap1200))
            ]
        else:
            raise ValueError("Длина поезда (l) должна быть меньше 1600")


        # Create and return the generator from the calculated list
        return generator_func(thetasost_list)

    # Результаты будут записываться в список
    results = []
    thetasost_gen = calculate_percent(l)

    # Цикл по интервалам времени
    while Vn > 0:
        # Получаем текущее значение thetasost
        thetasost = next(thetasost_gen)

        # Рассчитываем thetachrf и thetakrf
        thetachrf = thetachr * (thetasost / 100)
        thetakrf = thetakr * (thetasost / 100)

        # Цикл внутри цикла для определения Vcp
        Vcp = Vn
        step = 10.0
        lastError = 10000.0
        while True:
            Vp = Vcp
            Fchkr = 0.27 * ((Vp + 100) / (5 * Vp + 100))
            Fkkr = 0.36 * ((Vp + 150) / (2 * Vp + 150))
            bcht = 1000 * thetachrf * Fchkr
            bkt = 1000 * thetakrf * Fkkr
            bt = bcht + bkt

            wox = 2.4 + 0.011 * Vp + 0.00035 * Vp ** 2
            wo = A + B * Vp + C * Vp ** 2
            w = (wo * Q + wox * P) / (P + Q)

            dV = -((u * (bt + w + i)) / 3600) * dt
            Vk = Vn + dV
            if Vk < 0:
                Vk = 0
            Vcp = (Vn + Vk) / 2

            newError = abs(Vcp - Vp)
            if newError >= lastError:
                Vcp += step
                step /= -2
            lastError = newError

            if newError <= 0.5:
                break

        dS = 0.278 * Vcp * dt
        dΣS = dS if not results else dS + results[-1][-1]
        results.append((
            f"{len(results) + 1}", f"{dt * len(results)}-{dt * (len(results) + 1)}", thetasost,
            thetachrf, thetakrf, Vp, Fchkr, bcht, Fkkr, bkt, bt, wo, wox, w,
            Vn, dV, Vk, Vcp, dS, dΣS
        ))

        Vn = Vk

    # Создаем DataFrame и выводим результаты
    columns = [
        "№ интервала", "Интервал", "ϑсост", "ϑчрф", "ϑкрф", "Vp", "Фчкр", "bчт",
        "Фккр", "bкт", "bт", "wo", "wox", "w",
        "Vн", "dV", "Vк", "Vср", "dS", "dΣS"
    ]
    df = pd.DataFrame(results, columns=columns)
    return df


