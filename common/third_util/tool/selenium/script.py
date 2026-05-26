from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from common.util.export import List, logger


class SeleniumScript:
    def __init__(self, driver):
        self.driver = driver

    def scroll_into_view(self, ele: WebElement):
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)

    def script_click(self, ele: WebElement):
        self.driver.execute_script("arguments[0].click();", ele)

    def get_xpath_from_devtools(self, element: WebElement) -> str:
        js_code = """
        function getXPathForElement(element) {
            const idx = (sib, name) => sib 
                ? idx(sib.previousElementSibling, name||sib.localName) + (sib.localName == name)
                : 1;
            const segs = elm => !elm || elm.nodeType !== 1 
                ? ['']
                : elm.id && document.getElementById(elm.id) === elm
                    ? [`//*[@id="${elm.id}"]`]
                    : [...segs(elm.parentNode), `${elm.localName.toLowerCase()}[${idx(elm)}]`];
            return segs(element).join('/');
        }
        return getXPathForElement(arguments[0]);
        """
        return self.driver.execute_script(js_code, element)

    def e_format(self, element: WebElement, text_max_size=20) -> str:
        if isinstance(element, list):
            rets = []
            for e in element:
                rets.append(self._e_format_node(e, text_max_size))
            return "\n".join(rets)
        return self._e_format_node(element, text_max_size)

    def _e_format_node(self, element: WebElement, text_max_size=20) -> str:
        ret = []
        element_id = element.get_attribute("id")
        tag_name = element.tag_name
        class_attr = element.get_attribute("class") or ""
        name_attr = element.get_attribute("name") or ""
        url = element.get_attribute("url") or ""
        title = element.get_attribute("title") or ""
        disabled = element.get_attribute("disabled")

        location_str = ""
        try:
            location = element.location
            size = element.size
            location_str = f"位置: ({location['x']}, {location['y']}); 大小: {size['width']}x{size['height']}"
        except Exception:
            pass

        try:
            text = element.text.strip()
            if len(text) > text_max_size * 2:
                text = text[:text_max_size] + "..." + text[-text_max_size:]
        except Exception:
            text = ""

        ret.append("; ".join([
            f"标签: <{tag_name}>",
            f"ID: [{element_id}]",
            f"title: [{title}]",
            f"disabled: [{disabled}]",
            f"type: [{element.get_attribute('type')}]",
        ]))
        ret.append(f"   XPATH:{self.get_xpath_from_devtools(element)} ")
        if class_attr:
            ret.append(f"   类: {class_attr};")
        if name_attr:
            ret.append(f"   Name: {name_attr}")
        if url:
            ret.append(f"   uri: {url}")
        ret.append(f"   {location_str}")
        if text:
            ret.append(f"   文本: {text}")

        return "\n".join(ret)

    def wait_doc_ready(self, wait: WebDriverWait):
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")