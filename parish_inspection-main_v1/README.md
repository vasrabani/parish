### Update V3
- Views.py is now modified to be class based instead of function based.
- Improved register and login page UI
- For each Parish creation, a profile pic default or user uploaded will be shown.
- In Parish details page, the UI is better now and Number of inspections as well as reference is shown (starting from oldest to newest).
- Admin has control over all parishes and inspections (CRUD)
- Questions UI is better, fixed where certain answers where not appearing.
- Edit inspection UI now shows the questions as well (not just the topics as before).
- Delete option confirmation page is made.
- Options for question responses are now "yes", "no", and "other", can make general comments at the end
- Pagination on homepage
- UI better for all pages.
- Option to remove parishes.
- A return to button in parish and inspection page, to go back to previous page.
#### Things to consider for next update
- Signals is incorporated, however more questions in "Questions" section in admin page get appended each time any user creates or edits an inspection, because the questions and answers are saved for the user and its own set gets added to the previous set. One proposal is to categorize all questions and store the responses for each static category for each user (the admin can edit the questions in admin), each user to have their own set of ONLY responses for EACH of their inspection. Have to look into this**
- Be able to modify profile pic in parish detail page anytime.
- Questions answers selectable must be set right to add "other" instead of "dont know".
### Example UI
<img src="https://github.com/KrishT97/parish_inspection/blob/main/extras/home.jpg" width="800"/>
<img src="https://github.com/KrishT97/parish_inspection/blob/main/extras/fancyparish.jpg" width="800"/>
