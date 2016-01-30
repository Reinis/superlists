from selenium import webdriver
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # User opens the home page of our to-do app
        self.browser.get('http://localhost:8000')

        # The page title and header metion to-do
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # There is an option to enter a to-do item stright away

        # She types "Buy peacock feathers" into a textbox

        # When she hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list

        # There is still a textbox inviting her to enter another item. She
        # enters "Use peacock feathers to make a fly"

        # The page updates again, and now shows both items on her list

        # She wonders whether the site remembers her list. Then she sees
        # that the site has generated a unique URL for her -- there is some
        # explanatory text to that effect.

        # She visits that URL - her to-do list is still there

        # Satisfied she goes back to sleep

if __name__ == '__main__':
    unittest.main()

