import requests
import json
from bs4 import BeautifulSoup
from criterion import criterion

def getData(username, key):
    url = "https://lostark.game.onstove.com/Profile/Character/" + username
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        contents = ""
        color = 0x00ff56
        
        # 기준
        criteria = criterion[key]

        # 클래스
        className = soup.select_one("#lostark-wrapper > div > main > div > div.profile-character-info > img").attrs['alt']

        # 아이템 레벨
        itemLevel = soup.select_one("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)").get_text()[3:]
        itemLevel = itemLevel.replace(",", "")
        if float(itemLevel) >= criteria["레벨"]:
            contents += ":white_check_mark:"
        else:
            color = 0xFF0000
            contents += ":x:"
        contents += " [레벨] " + itemLevel + "\n"

        # 원정대 레벨
        expeditionLevel = soup.select_one("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__expedition > span:nth-child(2)").get_text()[3:]
        if int(expeditionLevel) >= criteria["원정대"]:
            contents += ":white_check_mark:"
        else:
            color = 0xFF0000
            contents += ":x:"
        contents += " [원정대] " + expeditionLevel + "\n"

        # Script 데이터
        scriptData = soup.select_one("#profile-ability > script")

        cardSetStartIdx = str(scriptData).find('"CardSet":')
        equipStartIdx = str(scriptData).find('"Equip":')
        skillStartIdx = str(scriptData).find('"Skill":')

        cardSetStr = str(scriptData)[cardSetStartIdx:equipStartIdx]
        equipStr = str(scriptData)[equipStartIdx:skillStartIdx]

        # 무기 강화
        try:
            weaponCode = soup.select_one("#profile-equipment > div.profile-equipment__slot > div.slot6").attrs['data-item']
            weaponLevelStartIdx = equipStr.find(weaponCode) + 132
            weaponLevelStr = equipStr[weaponLevelStartIdx:weaponLevelStartIdx + 5].split()[0]
            weaponLevel = int(weaponLevelStr)
        except KeyError:
            weaponLevel = -1
        except ValueError:
            weaponLevel = 0

        if weaponLevel >= criteria["무기"]:
            contents += ":white_check_mark:"
            contents += " [무기] " + str(weaponLevel) + "강\n"
        elif weaponLevel == -1:
            color = 0xFF0000
            contents += ":x: [무기] 장착 안함\n"
        else:
            color = 0xFF0000
            contents += ":x:"
            contents += " [무기] " + str(weaponLevel) + "강\n"
        
        # 전투 특성
        try:
            invalidAbility1 = int(soup.select_one("#profile-ability > div.profile-ability-battle > ul > li:nth-child(3) > span:nth-child(2)").get_text())
            invalidAbility2 = int(soup.select_one("#profile-ability > div.profile-ability-battle > ul > li:nth-child(5) > span:nth-child(2)").get_text())
            invalidAbility3 = int(soup.select_one("#profile-ability > div.profile-ability-battle > ul > li:nth-child(6) > span:nth-child(2)").get_text())

            if max(invalidAbility1, invalidAbility2, invalidAbility3) >= 100:
                color = 0xFF0000
                contents += ":x: [전투 특성] 제인숙 있음\n"
        except:
            pass

        # 각인
        abilityTextList = soup.select("#profile-ability > div.profile-ability-engrave > div > div.swiper-wrapper > ul.swiper-slide > li > span")
        abilityList = []
        debuffList = []
        for ability in abilityTextList:
            if ability.get_text().find("감소") == -1:
                abilityList.append(int(ability.get_text()[-1]))
            else:
                debuffList.append(int(ability.get_text()[-1]))
        if sum(abilityList) >= criteria["각인"]:
            contents += ":white_check_mark:"
        else:
            color = 0xFF0000
            contents += ":x:"
        contents += " [각인] " + " ".join(map(str, abilityList))
        if debuffList:
            contents += " / 디버프 " + " ".join(map(str, debuffList))
        contents += "\n"

        # 보석
        tempIdx = 0
        jewelLevelList = []

        while True:
            mJewelIdx = equipStr.find("레벨 멸화", tempIdx)
            hJewelIdx = equipStr.find("레벨 홍염", tempIdx)
            jewelIdx = 0
            if mJewelIdx == -1 and hJewelIdx == -1:
                break
            if mJewelIdx == -1 and hJewelIdx != -1:
                jewelIdx = hJewelIdx
            elif mJewelIdx != -1 and hJewelIdx == -1:
                jewelIdx = mJewelIdx
            else:
                jewelIdx = min(hJewelIdx, mJewelIdx)
            jewelLevelList.append(10 if int(equipStr[jewelIdx - 1]) == 0 else int(equipStr[jewelIdx - 1]))
            tempIdx = jewelIdx + 1

        jewelAvg = sum(jewelLevelList) / 11.0
        if jewelAvg >= criteria["보석"]:
            contents += ":white_check_mark:"
        elif (className == "스카우터" or className == "데모닉") and jewelAvg >= (criteria["보석"] * 2.0 / 11.0):
            contents += ":mag:"
        else:
            color = 0xFF0000
            contents += ":x:"
        contents += " [보석] " + str(len(jewelLevelList)) + "개 / " + " ".join(map(str, jewelLevelList)) + "\n"

        # 트포작
        tempIdx = 0
        tripodLv4Cnt = 0
        tripodLv3Cnt = 0
        
        while True:
            tripodIdx = equipStr.find("Lv +", tempIdx)
            if tripodIdx == -1:
                break
            elif equipStr[tripodIdx + 4] == "4":
                tripodLv4Cnt += 1
            elif equipStr[tripodIdx + 4] == "3":
                tripodLv3Cnt += 1
            tempIdx = tripodIdx + 1

        if tripodLv4Cnt >= criteria["트포작"][0] and tripodLv3Cnt >= criteria["트포작"][1]:
            contents += ":white_check_mark:"
        else:
            color = 0xFF0000
            contents += ":x:"
        contents += " [트포작] Lv.4 " + str(tripodLv4Cnt) + "개 / Lv.3 " + str(tripodLv3Cnt) + "개\n"

        # 카드
        cardSetTextList = soup.select("#cardSetList > li")
        cardSetList = []
        addedIndexes = []

        for cardSet in reversed(cardSetTextList):
            if not cardSet.attrs["data-cardsetindex"] in addedIndexes:
                addedIndexes.append(cardSet.attrs["data-cardsetindex"])
                cardSetList.append(cardSet.select_one("div.card-effect__title").get_text())

        for i in range(len(cardSetList)):
            cardSetList[i] = cardSetList[i].replace("세상을 구하는 빛 6세트 (30각성합계)", "세구빛 30각")
            cardSetList[i] = cardSetList[i].replace("세상을 구하는 빛 6세트 (18각성합계)", "세구빛 18각")
            cardSetList[i] = cardSetList[i].replace("세상을 구하는 빛 6세트 (12각성합계)", "세구빛 12각")
            cardSetList[i] = cardSetList[i].replace("남겨진 바람의 절벽 6세트 (30각성합계)", "남바절 30각")
            cardSetList[i] = cardSetList[i].replace("남겨진 바람의 절벽 6세트 (12각성합계)", "남바절 12각")
            cardSetList[i] = cardSetList[i].replace("침묵하는 거인의 숲 3세트 (15각성합계)", "침거숲 15각")
            cardSetList[i] = cardSetList[i].replace("침묵하는 거인의 숲 3세트 (9각성합계)", "침거숲 9각")
            cardSetList[i] = cardSetList[i].replace("침묵하는 거인의 숲 3세트", "침거숲")
            cardSetList[i] = cardSetList[i].replace("살아서 다시 보길 바란다 3세트 (15각성합계)", "살다보 15각")
            cardSetList[i] = cardSetList[i].replace("살아서 다시 보길 바란다 3세트 (9각성합계)", "살다보 9각")
            cardSetList[i] = cardSetList[i].replace("살아서 다시 보길 바란다 3세트", "살다보")

        if cardSetList:
            contents += ":mag: [카드] " + ", ".join(cardSetList) + "\n"
        else:
            color = 0xFF0000
            contents += ":x: [카드] 없음\n"
        
        return className, contents, color
    else:
        return "response error!"