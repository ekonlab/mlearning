import simplejson as json

def lazyLineJsonReader(filebuffer, nlines=None):
  """
    Lazy function (generator) to read a file line by line.
    File needs to be on lineformat
  """
  
  i = 0
  while True:
    line = filebuffer.readline()
    if not line or i == nlines:
      filebuffer.close()
      break
    i += 1
    yield json.loads(line)
    

def split_in_files(filename,linesXfile=100000):
  i = 0
  size = 0
  chunk = []
  for line in lazyLineJsonReader(open(filename)):
    chunk.append(line)
    size += 1
    if size == linesXfile:
      output_name = filename.split('.json')[0] + '_ch'+str(i)+'.json'
      with open(output_name,'w') as o:
        json.dump(chunk, o)
        i += 1
        print('writing file ', output_name)
      
      chunk = []
      size = 0
      
if __name__ == '__main__':
  split_in_files('suspects.json')
