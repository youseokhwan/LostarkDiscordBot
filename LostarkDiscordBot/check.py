import requests
import json
from bs4 import BeautifulSoup

def getData(username):
    url = "https://lostark.game.onstove.com/Profile/Character/" + username
    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        contents = ""
        color = 0x00ff56
        
        # 클래스
        className = soup.select_one("#lostark-wrapper > div > main > div > div.profile-character-info > img").attrs['alt']

        # 아이템 레벨
        itemLevel = soup.select_one("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info2 > div.level-info2__expedition > span:nth-child(2)").get_text()[3:]
        itemLevel = itemLevel.replace(",", "")
        if float(itemLevel) >= 1415.0:
            contents += ":white_check_mark:"
        else:
            color = 0xFF0000
            contents += ":x:"
        contents += " [레벨] " + itemLevel + "\n"

        # 원정대 레벨
        expeditionLevel = soup.select_one("#lostark-wrapper > div > main > div > div.profile-ingame > div.profile-info > div.level-info > div.level-info__expedition > span:nth-child(2)").get_text()[3:]
        if int(expeditionLevel) >= 100:
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

        # 무기 코드
        weaponCode = soup.select_one("#profile-equipment > div.profile-equipment__slot > div.slot6").attrs['data-item']

        # 무기 강화
        weaponLevelStartIdx = equipStr.find(weaponCode) + 132
        weaponLevel = equipStr[weaponLevelStartIdx:weaponLevelStartIdx + 5].split()[0]
        if int(weaponLevel) >= 17:
            contents += ":white_check_mark:"
        else:
            color = 0xFF0000
            contents += ":x:"
        contents += " [무기] " + weaponLevel + "강\n"

        # 각인
        abilityTextList = soup.select("#profile-ability > div.profile-ability-engrave > div > div.swiper-wrapper > ul.swiper-slide > li > span")
        abilityList = []
        debuffList = []
        for ability in abilityTextList:
            if ability.get_text().find("감소") == -1:
                abilityList.append(int(ability.get_text()[-1]))
            else:
                debuffList.append(int(ability.get_text()[-1]))
        if sum(abilityList) >= 12:
            contents += ":white_check_mark:"
        else:
            color = 0xFF0000
            contents += ":x:"
        contents += " [각인] " + "".join(map(str, abilityList))
        if debuffList:
            contents += " / 디버프 " + "".join(map(str, debuffList))
        contents += "\n"

        # 카드
        cardSetTextList = soup.select("#cardSetList > li")
        cardSetList = []
        addedIndexes = []
        for cardSet in reversed(cardSetTextList):
            if not cardSet.attrs["data-cardsetindex"] in addedIndexes:
                addedIndexes.append(cardSet.attrs["data-cardsetindex"])
                cardSetList.append(cardSet.select_one("div.card-effect__title").get_text())
        if cardSetList:
            contents += ":mag: [카드] " + ", ".join(cardSetList) + "\n"
        else:
            color = 0xFF0000
            contents += ":x: [카드] 없음\n"

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
            jewelLevelList.append(int(equipStr[jewelIdx - 1]))
            tempIdx = jewelIdx + 1
        print(jewelLevelList)

        if sum(jewelLevelList) / 11.0 >= 5.0:
            contents += ":white_check_mark:"
        elif className == "스카우터" or className == "데모닉":
            contents += ":mag:"
        else:
            contents += ":x:"
        contents += " [보석] " + "".join(map(str, jewelLevelList)) + "\n"

        # 트포작
        contents += ":grey_question: [트포작] 미구현\n"
        
        return className, contents, color
    else:
        return "response error!"