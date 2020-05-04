import re

class ReExtractor:

    def extract_timetable_info(self, info):
        table = [[] for i in range(7)]
        for row in info:
            for i, col in enumerate(row):
                matches = re.findall("(.*)\\n(.*)\\n(\d+)-(\d+)(\\([单双]\\))?周 (\d+)-(\d+)节", col.strip())
                for match in matches:
                    table[i].append(match)
        return table

    # "(.*)\\n(.*)\\n(\d+)-(\d+)(\\([单双]\\))?周 (\d+)-(\d+)节"