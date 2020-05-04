from flask import Flask, request, jsonify

from utils.SeleniumUtils import SsfwExtractor
from utils.ReUtils import ReExtractor

table_extractor = SsfwExtractor()
re_extractor = ReExtractor()

app = Flask(__name__)


@app.route('/pull_timetable', methods=["POST"])
def pull():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if username == "test":
        ext_table = table_extractor.testFor()
    else:
        try:
            table_extractor.login(username, password)
            ext_table = table_extractor.extract_timetable()
        except Exception as e:
            return {"error": e}
    table = re_extractor.extract_timetable_info(ext_table)

    return {'timetable': table}


if __name__ == '__main__':
    app.run()
