# Educative-Content-Extracter
Script written using Python and Selenium that automatically extracts the content of all lessons of a course on Educative platform into a text file.

## Pre-requisites
* Selenium should be installed on your machine. You can install it via: `pip install selenium` or `pip3 install selenium`
* chromedriver should also be installed. You can install it via: `brew install chromedriver`. If you do not have brew installed on your mac you can install and set it up from here: https://brew.sh/
* Install `getpass` module via: `pip install getpass4` or `pip3 install getpass4`
* Install `webdriver-manager` module via: `pip install webdriver-manager` or `pip3 install webdriver-manager`
* When you run the script, you might receive an error that chromedriver is not trusted. Please follow the following link in order to fix this error: https://timonweb.com/misc/fixing-error-chromedriver-cannot-be-opened-because-the-developer-cannot-be-verified-unable-to-launch-the-chrome-browser-on-mac-os/
* If you receive an incorrect chromedriver error, please download the correct version according to your chrome browser version from here: https://chromedriver.storage.googleapis.com/index.html

## Running the script
* Clone the repository: https://github.com/raahimkhan/Educative-Course-Content-Extracter.git or download it as a zip file.
* cd into the `Educative-Course-Content-Extracter` directory.
* Run: `python3 extracter.py` or `python extracter.py`
* Follow the instructions on the terminal to successfully scrape the contents of the entire course into a text file.
* Contents will be written to `course.txt` file.

## Format
* Lesson title (h1 heading extracted into text file)
* Lesson content (contents of p tags of lessons extracted to text file)
* Now the contents of TOCs is extracted into the text file
* Now the contents of bullet points are extracted. These are bullet points in the form of `li` tags inside the lesson
* Then the process repeats for all the other lessons inside the course and whole course is scrapped into one text file.

## Blockers
* Contents of code blocks and code widgets inside the lessons are not extracted.
* Grammarly only allows 1000 characters or 60 pages per submission. You can check the plagiarism of course using turnitin or any other alternative software.
