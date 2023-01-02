# Educative-Content-Extracter
Script written using Python and Selenium that automatically extracts the content of lessons of a course on Educative platform into a text file.

## Important pointers
* When you run the script, you might receive an error that chromedriver is not trusted. Please follow the following link in order to fix this error: https://timonweb.com/misc/fixing-error-chromedriver-cannot-be-opened-because-the-developer-cannot-be-verified-unable-to-launch-the-chrome-browser-on-mac-os/
* Execution time and speed of the script depends on your internet connection Hence, content scraping will fail if connection speed is slow.
  * Run `python3 extracter.py --help` to see available command-line arguments that can be modified to control the waiting times of the script.
  * For instance, to increase login validation timer, execute the script as `python3 extracter.py --validationTimer 20`. This will increase the login validation timer to 20 seconds. Execute `python3 extracter.py --help` to see more such modifications.

## Running the script
**Note:** Replace `pip3` with `pip` inside the `script.sh` file if your machine does not recognize `pip3`.
Execute the following commands to run the content extraction script successfully:
1) **Clone the repository:** `git clone https://github.com/raahimkhan/Educative-Content-Extracter.git`
2) **Navigate to the `Educative-Content-Extracter` directory:** `cd Educative-Content-Extracter`
3) **Make the `script.sh` file executable:** `chmod u+x script.sh`
4) **Execute `script.sh` file to setup and install dependencies:** `source script.sh`
5) **Run program:** `python3 extracter.py`
Now follow the instructions on the terminal to successfully scrape the contents of the course into a text file. Contents will be written to `course.txt` file

## Format
* Lesson title (h1 heading extracted into text file)
* Lesson content (contents of p tags of lessons extracted to text file)
* Now the contents of TOCs is extracted into the text file
* Now the contents of bullet points are extracted. These are bullet points in the form of `li` tags inside the lesson
* Then the process repeats for all the other lessons inside the course and whole course is scrapped into one text file

## Limitations
* Content of code blocks, code widgets, SPA, etc are not extracted
* Latex will not be extracted
* Content of projects, mini-projects, assessments, and quizzes are not extracted
* Works only for courses as of now. Does not work for paths, learning plans, skill assessments, etc
