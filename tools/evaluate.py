__author__ = "Zangue"

import subprocess
import time, sys

from random import shuffle

BASE_URL = "http://localhost:8080/samples/live-streaming"
URL = BASE_URL + "/%s?scheme=%s&proxy=%s&livesimulator=%s&segment_duration=%s&algo=%s&omega=%d&sigma=%d&test_nr=%d&run_nr=%d&delay=%d&report=1"

RUNS = 5
RUN_DURATION_SEC = 5 * 60

delays = [5]
sigmas = [50] # in %
omegas = [4] # in %

schemes = ['http', 'http']
proxies = ['192.168.10.190', '127.0.0.1:3000'] # change port
segment_durations = ['500ms', '750ms', '1s', '2s']
livesimulators = ['livesim_http1_custom', 'livesim_http2', 'livesim_no_push']

assert len(sigmas) == len(omegas), "Omegas and sigmas arrays have not the same element count"

test_count = len(sigmas)

def open_chrome(url):
  cmd = ["google-chrome", "-incognito", "--new-window", url]
  sp = subprocess.Popen(cmd, stdout=subprocess.PIPE)
  #retval = sp.communicate()[0]
  #print sp.returncode
  #assert sp.returncode == 0 or 1, "Ran into an issue while opening chrome browser"
  #return sp.returncode

def close_chrome():
  sp = subprocess.Popen(["killall", "chrome"], stdout=subprocess.PIPE)
  retval = sp.communicate()[0]
  print sp.returncode
  assert sp.returncode == 0 or 1, "Ran into an issue while closing chrome browser"
  return sp.returncode

# Test Start

if __name__ == "__main__":
  close_chrome()
  print "Start Testing ..."
  global algos
  algos = ['lolypop']
  tc = 0
  # For every config, run test x time
  while tc < test_count:
    count = 0
    # Constants
    omega = omegas[0]
    sigma = sigmas[0]
    delay = delays[0]

    print "Test config omega: %d - sigma: %d - delay: %d sec" % (omega, sigma, delay)
    print "%d run(s) for each algo" % RUNS
    while count < RUNS:
      for scheme in schemes:
        if scheme == schemes[-1]:
          print ''
        for proxy in proxies:
          # HTTP/1 needs no HTTP/2 request cancelling
          if scheme == schemes[0] and proxy == proxies[-1]: 
            continue
          if proxy == proxies[-1]:
            print ''
          for segment_duration in segment_durations:
            for livesimulator in livesimulators:
              # HTTP/1 tests
              if scheme == schemes[0] and not(livesimulator == 'livesim_http1_custom'):
                continue
              # HTTP/2 tests
              if scheme == schemes[-1] and livesimulator == 'livesim_http1_custom':
                continue
              # If nothing is pushed there is no need to cancel anything
              # Take out proxy for no push tests
              if scheme == schemes[-1] and livesimulator == 'livesim_no_push' and proxy == proxies[-1]:
                continue
              # print 'Current test url' + scheme + "://192.168.10.190" + proxy + "/" + livesimulator + "/tfdt_1/sintel_" + segment_duration + "/Manifest.mpd"
              for algo in algos:
                test_nr = tc+1
                run_nr = count+1
                url = URL % ("lolypop.html", scheme, proxy, livesimulator, segment_duration, algo, omega, sigma, test_nr, run_nr, delay)
                print "Test URL %s" % url   
                open_chrome(url)
                print "Run test for %d seconds" % RUN_DURATION_SEC
                time.sleep(RUN_DURATION_SEC)
                close_chrome()
                print "Test done. Sleep 5 seconds ..."
                time.sleep(5)
                print "Woke up, continuing ..."
      count = count + 1
    tc = tc + 1
  print "Testing done :)"
  sys.exit(0)
