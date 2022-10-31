import math
from decimal import Decimal


class FormationCalculator:

    def getKareFormasyonHedefKonumlar(self, referans_noktasi, toplam_iha_sayisi, bireyler_arasi_mesafe):

        if toplam_iha_sayisi <= 4:

            konum1 = [0, 0]
            konum2 = [0, 0]
            konum3 = [0, 0]
            konum4 = [0, 0]

            bireyler_arasi_mesafe /= 2

            konum1[0] = referans_noktasi[0] + bireyler_arasi_mesafe
            konum1[1] = referans_noktasi[1] + bireyler_arasi_mesafe

            konum2[0] = referans_noktasi[0] + bireyler_arasi_mesafe
            konum2[1] = referans_noktasi[1] - bireyler_arasi_mesafe

            konum3[0] = referans_noktasi[0] - bireyler_arasi_mesafe
            konum3[1] = referans_noktasi[1] + bireyler_arasi_mesafe

            konum4[0] = referans_noktasi[0] - bireyler_arasi_mesafe
            konum4[1] = referans_noktasi[1] - bireyler_arasi_mesafe

            konumlar = [konum1, konum2, konum3, konum4]

            return konumlar
        else:

            koseler_disindaki_iha_sayisi = toplam_iha_sayisi - 4

            if koseler_disindaki_iha_sayisi % 4 > 0:
                ekleme = 1
            else:
                ekleme = 0

            koseler_arasi_mesafe = ((int(koseler_disindaki_iha_sayisi / 4) + ekleme) + 1) * bireyler_arasi_mesafe

            konum1 = [0, 0]
            konum2 = [0, 0]
            konum3 = [0, 0]
            konum4 = [0, 0]

            koseler_arasi_mesafe /= 2

            konum1[0] = referans_noktasi[0] + koseler_arasi_mesafe
            konum1[1] = referans_noktasi[1] + koseler_arasi_mesafe

            konum2[0] = referans_noktasi[0] + koseler_arasi_mesafe
            konum2[1] = referans_noktasi[1] - koseler_arasi_mesafe

            konum3[0] = referans_noktasi[0] - koseler_arasi_mesafe
            konum3[1] = referans_noktasi[1] + koseler_arasi_mesafe

            konum4[0] = referans_noktasi[0] - koseler_arasi_mesafe
            konum4[1] = referans_noktasi[1] - koseler_arasi_mesafe

            konumlar = [konum1, konum2, konum3, konum4]

            kenar1_iha_sayisi = 0
            kenar2_iha_sayisi = 0
            kenar3_iha_sayisi = 0
            kenar4_iha_sayisi = 0

            i = koseler_disindaki_iha_sayisi
            while i > 0:
                kenar1_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar2_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar3_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar4_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

            for i in range(kenar1_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum1[0]
                konum[1] = konum1[1] - bireyler_arasi_mesafe * (i + 1)
                konumlar.append(konum)

            for i in range(kenar2_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum2[0] - bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum2[1]
                konumlar.append(konum)

            for i in range(kenar3_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum3[0] + bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum3[1]
                konumlar.append(konum)

            for i in range(kenar4_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum4[0]
                konum[1] = konum4[1] + bireyler_arasi_mesafe * (i + 1)
                konumlar.append(konum)

            return konumlar

    def getUcgenFormasyonHedefKonumlar(self, referans_noktasi, toplam_iha_sayisi, bireyler_arasi_mesafe, aci1=0, aci2=0,
                                       aci3=0):

        if toplam_iha_sayisi <= 3:

            konum2 = [0, 0]
            konum3 = [0, 0]

            konum1 = [referans_noktasi[0], referans_noktasi[1] + (bireyler_arasi_mesafe / 2)]

            konum2[0] = konum1[0] + math.sin(math.radians(30)) * bireyler_arasi_mesafe
            konum2[1] = konum1[1] - math.cos(math.radians(30)) * bireyler_arasi_mesafe

            konum3[0] = konum1[0] + math.sin(math.radians(-30)) * bireyler_arasi_mesafe
            konum3[1] = konum1[1] - math.cos(math.radians(-30)) * bireyler_arasi_mesafe

            konumlar = [konum1, konum2, konum3]

            return konumlar
        else:

            koseler_disindaki_iha_sayisi = toplam_iha_sayisi - 3

            if koseler_disindaki_iha_sayisi % 3 > 0:
                ekleme = 1
            else:
                ekleme = 0

            koseler_arasi_mesafe = ((int(koseler_disindaki_iha_sayisi / 3) + ekleme) + 1) * bireyler_arasi_mesafe

            konum2 = [0, 0]
            konum3 = [0, 0]

            konum1 = [referans_noktasi[0], referans_noktasi[1] + (koseler_arasi_mesafe / 2)]

            konum2[0] = konum1[0] + math.sin(math.radians(30)) * koseler_arasi_mesafe
            konum2[1] = konum1[1] - math.cos(math.radians(30)) * koseler_arasi_mesafe

            konum3[0] = konum1[0] + math.sin(math.radians(-30)) * koseler_arasi_mesafe
            konum3[1] = konum1[1] - math.cos(math.radians(-30)) * koseler_arasi_mesafe

            konumlar = [konum1, konum2, konum3]

            kenar1_iha_sayisi = 0
            kenar2_iha_sayisi = 0
            kenar3_iha_sayisi = 0

            i = koseler_disindaki_iha_sayisi
            while i > 0:
                kenar1_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar2_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar3_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

            for i in range(kenar1_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum1[0] + math.sin(math.radians(30)) * bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum1[1] - math.cos(math.radians(30)) * bireyler_arasi_mesafe * (i + 1)
                konumlar.append(konum)

            for i in range(kenar2_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum1[0] + math.sin(math.radians(-30)) * bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum1[1] - math.cos(math.radians(-30)) * bireyler_arasi_mesafe * (i + 1)
                konumlar.append(konum)

            for i in range(kenar3_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum3[0] + bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum3[1]
                konumlar.append(konum)

            return konumlar

    def getBesgenFormasyonHedefKonumlar(self, referans_noktasi, toplam_iha_sayisi, bireyler_arasi_mesafe):

        if toplam_iha_sayisi <= 5:

            konum2 = [0, 0]
            konum3 = [0, 0]
            konum4 = [0, 0]
            konum5 = [0, 0]

            konum1 = [referans_noktasi[0], referans_noktasi[1] + bireyler_arasi_mesafe]

            konum2[0] = konum1[0] + math.sin(math.radians(54)) * bireyler_arasi_mesafe
            konum2[1] = konum1[1] - math.cos(math.radians(54)) * bireyler_arasi_mesafe

            konum3[0] = konum1[0] + math.sin(math.radians(-54)) * bireyler_arasi_mesafe
            konum3[1] = konum1[1] - math.cos(math.radians(-54)) * bireyler_arasi_mesafe

            konum4[0] = konum2[0] + math.sin(math.radians(-18)) * bireyler_arasi_mesafe
            konum4[1] = konum2[1] - math.cos(math.radians(-18)) * bireyler_arasi_mesafe

            konum5[0] = konum3[0] + math.sin(math.radians(18)) * bireyler_arasi_mesafe
            konum5[1] = konum3[1] - math.cos(math.radians(18)) * bireyler_arasi_mesafe

            konumlar = [konum1, konum2, konum3, konum4, konum5]

            return konumlar
        else:

            koseler_disindaki_iha_sayisi = toplam_iha_sayisi - 5

            if koseler_disindaki_iha_sayisi % 5 > 0:
                ekleme = 1
            else:
                ekleme = 0

            koseler_arasi_mesafe = ((int(koseler_disindaki_iha_sayisi / 5) + ekleme) + 1) * bireyler_arasi_mesafe

            konum2 = [0, 0]
            konum3 = [0, 0]
            konum4 = [0, 0]
            konum5 = [0, 0]

            konum1 = [referans_noktasi[0], referans_noktasi[1] + koseler_arasi_mesafe]

            konum2[0] = konum1[0] + math.sin(math.radians(54)) * koseler_arasi_mesafe
            konum2[1] = konum1[1] - math.cos(math.radians(54)) * koseler_arasi_mesafe

            konum3[0] = konum1[0] + math.sin(math.radians(-54)) * koseler_arasi_mesafe
            konum3[1] = konum1[1] - math.cos(math.radians(-54)) * koseler_arasi_mesafe

            konum4[0] = konum2[0] + math.sin(math.radians(-18)) * koseler_arasi_mesafe
            konum4[1] = konum2[1] - math.cos(math.radians(-18)) * koseler_arasi_mesafe

            konum5[0] = konum3[0] + math.sin(math.radians(18)) * koseler_arasi_mesafe
            konum5[1] = konum3[1] - math.cos(math.radians(18)) * koseler_arasi_mesafe

            konumlar = [konum1, konum2, konum3, konum4, konum5]

            kenar1_iha_sayisi = 0
            kenar2_iha_sayisi = 0
            kenar3_iha_sayisi = 0
            kenar4_iha_sayisi = 0
            kenar5_iha_sayisi = 0

            i = koseler_disindaki_iha_sayisi
            while i > 0:
                kenar1_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar2_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar3_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar4_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

                kenar5_iha_sayisi += 1
                i -= 1
                if i == 0:
                    break

            for i in range(kenar1_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum1[0] + math.sin(math.radians(54)) * bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum1[1] - math.cos(math.radians(54)) * bireyler_arasi_mesafe * (i + 1)
                konumlar.append(konum)

            for i in range(kenar2_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum1[0] + math.sin(math.radians(-54)) * bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum1[1] - math.cos(math.radians(-54)) * bireyler_arasi_mesafe * (i + 1)
                konumlar.append(konum)

            for i in range(kenar3_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum2[0] + math.sin(math.radians(-18)) * bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum2[1] - math.cos(math.radians(-18)) * bireyler_arasi_mesafe * (i + 1)
                konumlar.append(konum)

            for i in range(kenar4_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum3[0] + math.sin(math.radians(18)) * bireyler_arasi_mesafe * (i + 1)
                konum[1] = konum3[1] - math.cos(math.radians(18)) * bireyler_arasi_mesafe * (i + 1)
                konumlar.append(konum)

            for i in range(kenar5_iha_sayisi):
                konum = [0, 0]
                konum[0] = konum4[0] - (bireyler_arasi_mesafe * (i + 1))
                konum[1] = konum4[1]
                konumlar.append(konum)

            return konumlar

    def getV_FormasyonHedefKonumlar(self, referans_noktasi, toplam_iha_sayisi, bireyler_arasi_mesafe, aci):

        konumlar = []

        koseler_arasi_iha_sayisi = int((toplam_iha_sayisi) / 2)

        konum1 = [referans_noktasi[0], referans_noktasi[1] - (int(toplam_iha_sayisi / 4) * bireyler_arasi_mesafe)]
        konumlar.append(konum1)

        for i in range(1, koseler_arasi_iha_sayisi + 1):
            konum = [0, 0]
            konum[0] = konum1[0] + math.sin(math.radians(180 + (aci / 2 * 1))) * bireyler_arasi_mesafe * i
            konum[1] = konum1[1] - math.cos(math.radians(180 + (aci / 2 * 1))) * bireyler_arasi_mesafe * i
            konumlar.append(konum)

            if len(konumlar) == toplam_iha_sayisi:
                break

            konum = [0, 0]
            konum[0] = konum1[0] + math.sin(math.radians(180 + (aci / 2 * -1))) * bireyler_arasi_mesafe * i
            konum[1] = konum1[1] - math.cos(math.radians(180 + (aci / 2 * -1))) * bireyler_arasi_mesafe * i
            konumlar.append(konum)

        return konumlar

    def getCemberFormasyonHedefKonumlar(self, referans_noktasi, toplam_iha_sayisi, yaricap):

        bireyler_arasi_aci = int(360 / toplam_iha_sayisi)
        konumlar = []
        aci = 0
        for i in range(0, toplam_iha_sayisi):
            aci = aci + bireyler_arasi_aci
            konum = [0, 0]
            konum[0] = referans_noktasi[0] + math.sin(math.radians(aci)) * yaricap
            konum[1] = referans_noktasi[1] - math.cos(math.radians(aci)) * yaricap

            if 0.01 > konum[0] > -0.01:
                konum[0] = 0
            if 0.01 > konum[1] > -0.01:
                konum[1] = 0

            konumlar.append(konum)

        return konumlar

    def getHilalFormasyonHedefKonumlar(self, referans_noktasi, toplam_iha_sayisi, yaricap):

        bireyler_arasi_aci = int(300 / toplam_iha_sayisi)
        konumlar = []
        aci = 0
        for i in range(0, toplam_iha_sayisi):
            aci = aci + bireyler_arasi_aci
            konum = [0, 0]
            konum[0] = referans_noktasi[0] + math.sin(math.radians(aci)) * yaricap
            konum[1] = referans_noktasi[1] - math.cos(math.radians(aci)) * yaricap

            if 0.01 > konum[0] > -0.01:
                konum[0] = 0
            if 0.01 > konum[1] > -0.01:
                konum[1] = 0

            konumlar.append(konum)

        return konumlar

    def getYildizFormasyonHedefKonumlar(self, referans_noktasi, toplam_iha_sayisi, bireyler_arasi_mesafe):

        konumlar = []

        koseler_arasi_iha_sayisi = int(toplam_iha_sayisi / 3)

        konum1 = [referans_noktasi[0], (referans_noktasi[1] + (bireyler_arasi_mesafe))]
        konumlar.append(konum1)

        for i in range(1, koseler_arasi_iha_sayisi):
            konum = [0, 0]
            konum[0] = konum1[0] + math.sin(math.radians(18)) * bireyler_arasi_mesafe * i
            konum[1] = konum1[1] - math.cos(math.radians(18)) * bireyler_arasi_mesafe * i
            konumlar.append(konum)

            konum = [0, 0]
            konum[0] = konum1[0] + math.sin(math.radians(-18)) * bireyler_arasi_mesafe * i
            konum[1] = konum1[1] - math.cos(math.radians(-18)) * bireyler_arasi_mesafe * i
            konumlar.append(konum)

        ref1 = konumlar[len(konumlar) - 1]
        ref2 = konumlar[len(konumlar) - 2]

        for i in range(1, koseler_arasi_iha_sayisi):
            konum = [0, 0]
            konum[0] = ref1[0] + math.sin(math.radians(126)) * bireyler_arasi_mesafe * i
            konum[1] = ref1[1] - math.cos(math.radians(126)) * bireyler_arasi_mesafe * i
            konumlar.append(konum)

            konum = [0, 0]
            konum[0] = ref2[0] + math.sin(math.radians(-126)) * bireyler_arasi_mesafe * i
            konum[1] = ref2[1] - math.cos(math.radians(-126)) * bireyler_arasi_mesafe * i
            konumlar.append(konum)

        ref3 = konumlar[len(konumlar) - 1]
        for i in range(1, koseler_arasi_iha_sayisi):
            konum = [0, 0]
            konum[0] = ref3[0] + math.sin(math.radians(90)) * bireyler_arasi_mesafe * i
            konum[1] = ref3[1] - math.cos(math.radians(90)) * bireyler_arasi_mesafe * i
            konumlar.append(konum)

        konumlar.pop(len(konumlar) - 1)
        return konumlar