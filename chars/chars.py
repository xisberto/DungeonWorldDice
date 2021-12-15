from replit import db


attrs = ['name', 'str', 'con', 'dex', 'int', 'wis', 'cha']

empty = {
    'player': '',
    'name': '',
    'str': '0',
    'con': '0',
    'dex': '0',
    'int': '0',
    'wis': '0',
    'cha': '0'
}

def load(player: str = None):
  if player is None:
    return empty
  if player not in db.keys():
    new = empty
    new['player'] = player
    db[player] = new
  return db[player]

def save(char):
  db[char['player']] = char

def delete(id: str):
  del db[id]
