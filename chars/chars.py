from replit import db

attrs = ['name', 'str', 'con', 'dex', 'int', 'wis', 'cha']

empty = {
    'id': '',
    'name': '',
    'str': '0',
    'con': '0',
    'dex': '0',
    'int': '0',
    'wis': '0',
    'cha': '0'
}


def load(char_id: str = None):
    if char_id is None:
        return empty
    if 'chars' not in db.keys():
        db['chars'] = []
    if char_id not in db['chars'].keys():
        new = empty
        new['id'] = char_id
        db['chars'][char_id] = new
    return db[char_id]


def save(char):
    db['chars'][char['id']] = char


def delete(char_id: str):
    del db['chars'][char_id]
