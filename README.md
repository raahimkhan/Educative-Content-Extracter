# Educative-Content-Extracter
Script written using Python and Selenium that automatically extracts the content of lessons of a course on Educative platform into a text file.

## Important pointer
* When you run the script, you might receive an error that chromedriver is not trusted. Please follow the following link in order to fix this error: https://timonweb.com/misc/fixing-error-chromedriver-cannot-be-opened-because-the-developer-cannot-be-verified-unable-to-launch-the-chrome-browser-on-mac-os/

## Running the script
**Note:** Replace `pip3` with `pip` in the commands below if the commands do not work with `pip3`
1) **Clone the repository:** `git clone https://github.com/raahimkhan/Educative-Content-Extracter.git`
2) **Navigate to the `Educative-Content-Extracter` directory:** `cd Educative-Content-Extracter`
3) **Install virtual environment (if not already installed):** `pip3 install virtualenv`
4) **Create virtual environment:** `python3 -m venv env`
5) **Enable virtual environment:** `source env/bin/activate`
6) **Upgrade `pip`:** `"env/bin/python3" -m pip install --upgrade pip`
7) **Install `wheel`:** `pip3 install wheel`
8) **Install required libraries and packages:** `pip3 install -r requirements.txt`
9) **Run program:** `python3 extracter.py`

Follow the instructions on the terminal to successfully scrape the contents of the course into a text file. Contents will be written to `course.txt` file

## Format
* Lesson title (h1 heading extracted into text file)
* Lesson content (contents of p tags of lessons extracted to text file)
* Now the contents of TOCs is extracted into the text file
* Now the contents of bullet points are extracted. These are bullet points in the form of `li` tags inside the lesson
* Then the process repeats for all the other lessons inside the course and whole course is scrapped into one text file

## Limitations
* Content of code blocks, code widgets, SPA, etc are not extracted
* Content of projects, mini-projects, assessments, and quizzes are not extracted
* Works only for courses as of now. Does not work for paths, learning plans, skill assessments, etc
