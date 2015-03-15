from selenium import webdriver
import time

URL = 'http://itv.brtn.cn/columndetail/index/21084'
FIRST_ONE = u'2013-12-19'

def start_browser():
  browser = webdriver.Chrome()
  browser.implicitly_wait(5)
  return browser

def open_index_page(browser, url):
  browser.get(url)

def scroll_to_the_end(browser):
  scroll_load_container = browser.find_element_by_id('scroll_load_container')

  current_childs = scroll_load_container.find_elements_by_class_name('date')
  while FIRST_ONE != current_childs[len(current_childs) - 1].text:
    scroll_load_container_child_number = len(current_childs)
    browser.execute_script('window.scrollTo(0,0);')
    time.sleep(3)
    browser.execute_script('window.scrollTo(0,Math.max(document.documentElement.scrollHeight,document.body.scrollHeight,document.documentElement.clientHeight));')
    time.sleep(3)
    current_childs = scroll_load_container.find_elements_by_class_name('date')
  print 'Reach to the end of the page and find ', len(current_childs), ' videos'

def parse_video_link(browser):
  scroll_load_container = browser.find_element_by_id('scroll_load_container')
  items = scroll_load_container.find_elements_by_class_name('pic1')
  guids = []
  image_url_prefix = 'http://media.bcloud.brtn.cn/'
  image_url_subfix = '/'
  for item in items:
    # http://media.bcloud.brtn.cn/dd/c0/ddc07ca2-029c-1793-b655-593b97e150ca/t.jpg_190_143.jpg
    src = item.get_attribute('src')
    guid = src[len(image_url_prefix) : src.rindex(image_url_subfix)]
    guids.append(guid)
  return guids


def save_video_links(guids):
  f = open('video_links.txt', 'w+')
  # http://video.bcloud.brtn.cn/[ee/83/ee837021-c485-88c0-a4f4-c709ae864468]/mp4h.mp4
  video_url_prefix = 'http://video.bcloud.brtn.cn/'
  video_url_subfix = '/mp4h.mp4'
  for guid in guids:
    f.write(video_url_prefix + guid + video_url_subfix)
    f.write('\n')

def close_browser(browser):
  browser.close()

def run():
  browser = start_browser()
  open_index_page(browser, URL)
  scroll_to_the_end(browser)
  guids = parse_video_link(browser)
  save_video_links(guids)
  close_browser(browser)

if __name__ == '__main__':
  run()
