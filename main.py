import psutil
import time
import csv
import keyboard

class Timer:
  def __init__(self, max):
    self.max = max
    self.last_reset = time.process_time()

  def run(self):
    next_reset = self.last_reset + self.max
    if time.process_time() >= next_reset:
      self.reset()
      return False
    else:
      return True

  def reset(self):
    self.last_reset = time.process_time()


class Datum:

  def __init__(self, used, available):
    self.used = used
    self.available = available
    self.seconds_since_epoch = time.time()


timer = Timer(max=1)
data = []
run = True
while run:
  used = psutil.virtual_memory().percent
  available = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total

  run = timer.run()
  if not run:
    datum = Datum(used, available)
    data.append(datum)
    print(f"Epoch: {datum.seconds_since_epoch} RAM Used:{datum.used}%, Available:{datum.available}%")
  run = (not keyboard.is_pressed('q'))

# Save to csv
fnames = ['epoch', 'used', 'available']
f = open('data.csv', 'w')
with f:
  writer = csv.DictWriter(f, fieldnames=fnames)
  writer.writeheader()
  for d in data:
    writer.writerow({'epoch': d.seconds_since_epoch,
                     'used': d.used,
                     'available': d.available})
