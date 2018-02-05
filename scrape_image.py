from selenium.webdriver import Firefox
import time
import boto3

def search_for_items(browser, search_term,login,pw):
    """search for key words at front page"""
    browser.get("https://www.pinterest.com/")
    time.sleep(2)
    log_in_button=browser.find_element_by_css_selector("button.lightGrey.active")
    log_in_button.click()
    time.sleep(2)
    emailElem = browser.find_element_by_css_selector('input#email')
    emailElem.send_keys(login)

    time.sleep(2)
    passwordElem = browser.find_element_by_css_selector('input#password')
    passwordElem.send_keys(pw)
    time.sleep(1)
    continue_button=browser.find_element_by_css_selector("button.red.SignupButton.active")
    continue_button.click()
    time.sleep(2)
    search_box_big=browser.find_element_by_css_selector("div._0._3i._2m._11._3w._2g._2i._2l._5e")
    search_box = search_box_big.find_element_by_css_selector("div._0._3i._2m._3e")
    search_box.click()
    time.sleep(1)
    search_box.send_keys(search_term)
    time.sleep(1)
    #search_box.send_keys('\n')




def find_images(browser):
    """Return image objects"""
    time.sleep(5)
    images = browser.find_elements_by_css_selector(
        "div.rg_bx a.rg_l img")
    return images

def scrape_image_upload(image, search_term, i):
    _ = image.location_once_scrolled_into_view
    image_url = image.get_attribute('src')
    photo_browser.get(image_url)
    image = photo_browser.find_element_by_css_selector(
        "img")
    image_png = image.screenshot_as_png
    label = "_".join(search_term.split())
    with open(f'image_{label}_{i}.png', 'wb') as f:
        f.write(image_png)
    remote_pathname="cap_stone/{}/{}_{}.png".format(label,label,i)
    file_name=f'image_{label}_{i}.png'
    save_to_s3(remote_pathname,file_name)

def scrape_images(images, search_term, photo_browser):
    for i, image in enumerate(images):
        time.sleep(1)
        scrape_image_upload(image, search_term, i)

def save_to_s3(remote_pathname,file_name):
    s3.upload_file(
    Bucket="input bucket name",
    Filename=file_name,
    Key=remote_pathname)


def search_scrape_save(search_terms):
    for search_term in search_terms:
        search_for_items(browser, search_term)
        images = find_images(browser)
        scrape_images(images, search_term, photo_browser)

if __name__=="__main__":
    browser = Firefox()
    photo_browser = Firefox()
    #s3 = boto3.client("s3")
    search_terms=["scandinavian interior design","scandinavian design","scandinavian living room",
"scandinavian bedroom","scandinavian decor ideas",
"scandinavian style kitchen",
"interior scandinavian style"]
    search_scrape_save(search_terms)
