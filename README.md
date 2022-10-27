# Educative-Content-Extracter
Script written using Python and Selenium that automatically extracts the content of all lessons of a course on Educative platform into a text file.

## Pre-requisites
* When you run the script, you might receive an error that chromedriver is not trusted. Please follow the following link in order to fix this error: https://timonweb.com/misc/fixing-error-chromedriver-cannot-be-opened-because-the-developer-cannot-be-verified-unable-to-launch-the-chrome-browser-on-mac-os/

## Running the script
* Clone the repository: https://github.com/raahimkhan/Educative-Content-Extracter.git
* cd into the `Educative-Content-Extracter` directory.
* Install virtual environment: `pip3 install virtualenv` or `pip install virtualenv`
* Create virtual environment: `python3 -m venv env` or `python -m venv env`
* Enable virtual environment: `source env/bin/activate`
* Install required libraries: `pip install -r requirements.txt` or `pip3 install -r requirements.txt`
* Run program: `python3 extracter.py` or `python extracter.py`
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
