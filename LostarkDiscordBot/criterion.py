import json
import pickle

with open("./data.txt", "rb") as f:
    criterion = pickle.load(f)

# criterion = {
#     "데칼": {"레벨": 1415.0, "원정대": 100, "무기": 15, "각인": 12, "보석": 5.0, "트포작": [0, 0]},
#     "아르고스1페": {"레벨": 1370.0, "원정대": 100, "무기": 15, "각인": 9, "보석": 5.0, "트포작": [0, 0]},
#     "아르고스3페": {"레벨": 1400.0, "원정대": 100, "무기": 15, "각인": 12, "보석": 5.0, "트포작": [0, 0]},
#     "발탄노말": {"레벨": 1415.0, "원정대": 100, "무기": 17, "각인": 12, "보석": 5.0, "트포작": [0, 0]},
#     "발탄하드": {"레벨": 1445.0, "원정대": 100, "무기": 19, "각인": 12, "보석": 5.0, "트포작": [6, 0]},
#     "비아노말": {"레벨": 1430.0, "원정대": 100, "무기": 18, "각인": 12, "보석": 5.0, "트포작": [6, 0]},
#     "비아하드": {"레벨": 1460.0, "원정대": 100, "무기": 20, "각인": 15, "보석": 5.0, "트포작": [6, 0]},
# }

# with open("./data.txt", "wb") as f:
#     pickle.dump(criterion, f)

def printHelp():
    return f"""
**1. 도움말 출력**
`!!`

**2. 닉네임 검색**
`!TypeSafe`

**3. 선택 가능한 기준**
{" ".join(map(wrapping, criterion.keys()))}

**4. 전체 기준 상세보기**
`!!!`

**5. 기준 추가**
`!!+쿤겔`

**6. 기준 수정**
`!!=쿤겔=무기=20`
`!!=쿤겔=트포작=6,0`

**7. 기준 삭제**
`!!-쿤겔`
    """

def printCriterion():
    return f"""
```json
{json.dumps(criterion, sort_keys=True, indent=4, ensure_ascii=False)}
```
"""

def wrapping(str):
    return "`!!" + str + "`"

def addCriterion(msg):
    msg = msg[3:]

    if msg in criterion:
        return f"`!!{msg}`은(는) 이미 존재하는 기준입니다."
    else:
        criterion[msg] = {"레벨": 0.0, "원정대": 0, "무기": 0, "각인": 0, "보석": 0.0, "트포작": [0, 0]}
        with open("./data.txt", "wb") as f:
            pickle.dump(criterion, f)
        return f"`!!{msg}`이(가) 추가되었습니다."

def updateCriterion(msg):
    msg = msg[3:]
    params = msg.split("=")
    
    if len(params) != 3:
        return "입력 포맷이 올바르지 않습니다."

    if params[0] in criterion:
        if params[1] in criterion[params[0]]:
            try:
                if params[1] == "트포작":
                    counts = params[2].split(",")
                    criterion[params[0]][params[1]] = [int(counts[0]), int(counts[1])]
                elif params[1] == "레벨" or params[1] == "보석":
                    criterion[params[0]][params[1]] = float(params[2])
                else:
                    criterion[params[0]][params[1]] = int(params[2])
                with open("./data.txt", "wb") as f:
                    pickle.dump(criterion, f)
                    return f"`!!{params[0]}`이(가) 수정되었습니다."
            except:
                return "오류가 발생했습니다."
        else:
            return f"`{params[1]}`은(는) 유효한 항목이 아닙니다."
    else:
        return f"`!!{msg}`은(는) 존재하지 않는 기준입니다."

def deleteCritirion(msg):
    msg = msg[3:]

    if msg in criterion:
        del(criterion[msg])
        with open("./data.txt", "wb") as f:
            pickle.dump(criterion, f)
        return f"`!!{msg}`이(가) 삭제되었습니다."
    else:
        return f"`!!{msg}`은(는) 존재하지 않는 기준입니다."