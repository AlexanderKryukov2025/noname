# import time
# import logging
# import urllib3
#
# from helpers.browser_logs import BrowserLogs
#
#
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#
# def wait_until_alert_is_present(drv, s=10):
#     try:
#         alert_is_present = WebDriverWait(drv, s).until(EC.alert_is_present())
#         if alert_is_present:
#             return drv.switch_to.alert
#
#     except EX.TimeoutException:
#         pass
#
#
# def wait_for_text_disappear(drv, loc, text=None, s=10):
#     timing = time.time()
#     while time.time() - timing < s * 3:
#         visible = wait_for_text(drv, loc, text, s)
#         if not visible:
#             return True
#
#
# def wait_for_text(drv, loc, text=None, attr=None, idx=0, s=10):
#     timing = time.time()
#     while time.time() - timing < s:
#         try:
#             elements = drv.find_elements(*loc)
#             # простой поиск среди всех элементов
#             if isinstance(text, str) and not attr:
#                 for e in elements:
#                     if text in e.text:
#                         return e.text
#
#             # ищет несколько совпадений в одной строке
#             elif isinstance(text, tuple):
#                 for e in elements:
#                     result = [t for t in text if str(t) in e.text]
#                     if len(result) >= len(text):
#                         return e.text
#
#             # ищет совпадения согласно порядку который задан списком
#             elif isinstance(text, list):
#                 for t in text:
#                     for e in elements:
#                         if t in e.text:
#                             return e.text
#
#             # ищет совпадения в аттрибутах элемента
#             elif isinstance(text, str):
#                 result = drv.execute_script(f'return document.querySelector("{loc[1]}").{attr}')
#                 if not result:
#                     continue
#
#                 if text and text in result:
#                     return result
#                 # если текст не указан, то вернет непустое текстовое содержимое локатора
#                 elif result:
#                     return result
#
#             else:
#                 # в этом случае достаточно чтобы строка была не пустой
#                 if len(elements) and elements[idx].text:
#                     return elements[idx].text
#
#         except (EX.StaleElementReferenceException, EX.NoSuchElementException, EX.JavascriptException):
#             pass
#
#
# def wait_text_in_curr_url(drv, text, endswith=False, s=10):
#     def get_result(text):
#         curr_url = drv.current_url
#         if endswith and curr_url.endswith(text):
#             return curr_url
#         else:
#             if text in curr_url:
#                 return curr_url
#
#     timing = time.time()
#     while time.time() - timing < s:
#         if isinstance(text, str):
#             r = get_result(text)
#             if r:
#                 return r
#
#         elif isinstance(text, list):
#             for t in text:
#                 r = get_result(t)
#                 if r:
#                     return r
#
#
# def get_elem_by_text(driver, loc, text=None, fullmatch=False, idx=0, s=25):
#     timing = time.time()  # конфигурация рабочая, не менять
#     while time.time() - timing < s:
#         try:
#             elements = driver.find_elements(*loc)
#             if isinstance(text, str):
#                 for e in elements:
#                     if ((text == e.text) if fullmatch else (text in e.text)):
#                         return e
#
#             # ищем совпадения согласно порядку который задан списком
#             elif isinstance(text, list):
#                 for t in text:
#                     for e in elements:
#                         if ((t == e.text) if fullmatch else (t in e.text)):
#                             return e
#
#             # ищем несколько совпадений в одной строке
#             elif isinstance(text, tuple):
#                 for e in elements:
#                     result = [s for s in text if str(s) in e.text]
#                     if len(result) >= len(text):
#                         return e
#
#             else:
#                 # в этом случае достаточно чтобы строка была не пустой
#                 if len(elements) and elements[idx].text:
#                     return elements[idx]
#         except:
#             pass
#
#
# def wait_until_file_download(drv, s=10):
#     drv.get('chrome://downloads/')
#     timing = time.time()
#     while time.time() - timing < s:
#         try:
#             results = []
#             for id_ in ['show', 'name', 'tag']:  # tag бывает таким - Failed - Needs authorization
#                 results.append(drv.execute_script(f"""
#                                 var result = document.querySelector('downloads-manager')
#                                     .shadowRoot.getElementById('frb0')
#                                     .shadowRoot.getElementById('{id_}').textContent;
#                                 return result;
#                                 """))
#             dnld_presence, dnld_filename, dnls_tag = results
#             if isinstance(dnld_presence, str):
#                 dnld_presence = dnld_presence.strip()
#             if dnld_presence in ['Show in folder', 'Показать в папке']:
#                 return dnld_filename + dnls_tag
#
#         except EX.JavascriptException:
#             pass
#     else:
#         pass
#
#
# def click_dwnld_and_wait_complete(drv, loc):
#     ts = round(time.time() * 1000)
#     wait_until_available(drv, loc).click()
#     bl = BrowserLogs(drv, ['Page.downloadProgress', '"state":"completed"'], ts=ts)
#
#     return bl.target_event
#
#
# def click_until_it_works(drv=None, loc=None, idx=None, s=10):
#     timing = time.time()
#     while time.time() - timing < s:
#         try:
#             if idx:
#                 drv.find_elements(*loc)[idx].click()
#                 return True
#
#             drv.find_element(*loc).click()
#             return True
#
#         except Exception as e:
#             report_error(loc, e)
#     else:
#         pass
#
#
# def wait_until_clickable(drv, loc, s=10):
#     return WebDriverWait(drv, s).until(EC.element_to_be_clickable(loc))
#
#
# def wait_until_present(drv, loc, s=10):
#     try:
#         return WebDriverWait(drv, s).until(EC.presence_of_element_located(loc))
#     except Exception as e:
#         report_error(loc, e)
#
#
# def wait_until_all_present(drv, loc, s=10):
#     try:
#         return WebDriverWait(drv, s).until(EC.presence_of_all_elements_located(loc))
#     except Exception as e:
#         report_error(loc, e)
#
#
# def wait_until_visible(drv, loc, s=10):
#     try:
#         return WebDriverWait(drv, s).until(EC.visibility_of_element_located(loc))
#     except Exception as e:
#         report_error(loc, e)
#
#
# def wait_until_invisible(drv, loc, s=10):
#     try:
#         return WebDriverWait(drv, s).until(EC.invisibility_of_element_located(loc))
#     except Exception as e:
#         report_error(loc, e)
#
#
# def wait_until_located(drv, loc, s=10):
#     try:
#         return WebDriverWait(drv, s).until(EC.visibility_of_all_elements_located(loc))
#     except Exception as e:
#         report_error(loc, e)
#
#
# def wait_until_text_present_in_element(drv, loc, text, s=10):
#     try:
#         return WebDriverWait(drv, s).until(EC.text_to_be_present_in_element(loc, text))
#     except Exception as e:
#         report_error(loc, e)
#
#
# def wait_until_text_present_in_element_value(drv, loc, text, s=10):
#     try:
#         return WebDriverWait(drv, s).until(EC.text_to_be_present_in_element_value(loc, text))
#     except Exception as e:
#         report_error(loc, e)
#
#
# def wait_until_text_present_in_element_attribute(drv, loc, attr, text, s=10):
#     try:
#         return WebDriverWait(drv, s).until(EC.text_to_be_present_in_element_attribute(loc, attr, text))
#     except Exception as e:
#         report_error(loc, e)
#
#
# def wait_until_display(drv, loc, elems=False, s=10):
#     timing = time.time()
#     while time.time() - timing < s:
#         try:
#             displayed = drv.find_element(*loc).is_displayed()
#             if not displayed:
#                 continue
#             else:
#                 if elems:
#                     return drv.find_elements(*loc)
#
#                 else:
#                     return drv.find_element(*loc)
#
#         except Exception as e:
#             report_error(loc, e)
#     else:
#         pass
#
#
# def wait_until_available(drv, loc, elems=False, s=10):
#     timing = time.time()
#     while time.time() - timing < s:
#         try:
#             if elems:
#                 elements = drv.find_elements(*loc)
#             else:
#                 elements = drv.find_element(*loc)
#             if not elements:
#                 continue
#
#             return elements
#         except (EX.NoSuchElementException, EX.StaleElementReferenceException) as e:
#             report_error(loc, e)
#     else:
#         pass
#
#
# def report_error(loc, e):
#     raise Exception(f'Element is unavailable:\n'
#                     f'Problem locator: {loc} \n'
#                     f'Exception: {e}')
#
#
# def page_load_timeout(drv, wait_for='complete', s=10):
#     """
#       "loading":
#             The document is still loading.
#       "interactive":
#             The document has finished loading. We can now access the DOM elements.
#             But sub-resources such as scripts, images, stylesheets and frames are still loading.
#       "complete":
#             The page is fully loaded.
#     """
#     timing = time.time()
#     while time.time() - timing < s:
#         state = drv.execute_script('return document.readyState;')
#         if wait_for == state:
#             break
