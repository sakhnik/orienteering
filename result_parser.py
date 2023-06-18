import xml.etree.ElementTree as ET
from collections import OrderedDict

ns = {"": "http://www.orienteering.org/datastandard/3.0"}


class Name:
    def __init__(self, el: ET.Element):
        self.id: int = int(el.find("./Person/Id", ns).text)
        self.family: str = el.find("./Person/Name/Family", ns).text
        self.given: str = el.find("./Person/Name/Given", ns).text
        self.club: str = el.find("./Organisation/Name", ns).text
        if not self.club:
            self.club = ""

    def full_name(self):
        return f"{self.family} {self.given}"

    def __hash__(self):
        return hash((self.family, self.given))

    def __eq__(self, other):
        return (self.family, self.given) == (other.family, other.given)

    def __ne__(self, other):
        return not (self == other)


def get_status(st: str) -> str:
    if st == "OK":
        return "OK"
    if st == "MissingPunch":
        return "MP"
    if st == "NotCompeting":
        return "NC"
    raise Exception(f"Unknown status {st}")


class Result:
    def __init__(self, el: ET.Element):
        self.name = Name(el)
        self.stage: int = 0
        self.time: float = float(el.find("./Result/Time", ns).text)
        self.time_behind: float = \
            float(el.find("./Result/TimeBehind", ns).text)
        self.rank: str = None
        try:
            self.position: int = int(el.find("./Result/Position", ns).text)
        except AttributeError:
            self.position: int = None
        self.status: str = get_status(el.find("./Result/Status", ns).text)


Competitors = list[Result]
ClassResults = OrderedDict[str, Competitors]


def Parse(fname: str) -> ClassResults:
    tree = ET.parse(fname)
    root = tree.getroot()
    class_results: ClassResults = OrderedDict()
    for class_res in root.findall("./ClassResult", ns):
        clname = class_res.find("./Class/Name", ns).text
        competitors = class_results.setdefault(clname, [])
        for person_res in class_res.findall("./PersonResult", ns):
            competitors.append(Result(person_res))
    return class_results
