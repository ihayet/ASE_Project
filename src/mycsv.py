from strings import coerce

def csv(sFilename):
  file = open(sFilename, 'r', encoding='utf-8')

  lines = file.readlines()
  cols = [[coerce(token.strip()) for token in lines[0].split(',')]]
  
  rows = []
  for i in range(1, len(lines)):
    rows.append([coerce(token.strip()) for token in lines[i].split(',')])

  return cols+rows
