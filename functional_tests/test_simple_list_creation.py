from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from .base import FunctionalTest


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User opens the home page of our to-do app
        self.browser.get(self.server_url)

        # The page title and header metion to-do
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # There is an option to enter a to-do item stright away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # She types "Buy peacock feathers" into a textbox
        inputbox.send_keys('Buy peacock feathers')

        # When she hits enter, she is taken to a new URL, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)

        list_url1 = self.browser.current_url
        self.assertRegex(list_url1, '/lists/.+')

        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # There is still a textbox inviting her to enter another item. She
        # enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

        # Now another user comes along to the site

        ## We use a new browser session to make sure that no information
        ## of the first user is comming trough from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # He visits home page. There is no sign of previous user's list.
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # He starts a new list by entering a new item. He is less interested
        # than the previous user...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # He gets his own unique URL
        list_url2 = self.browser.current_url
        self.assertRegex(list_url2, '/lists/.+')
        self.assertNotEqual(list_url2, list_url1)

        # Again, there is no trace of the previous user's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # Satisfied, they both go back to sleep

