# MAMA
(M)LS (A)dvanced (M)odule (A)ssigner

## Usage
### Creating the Students Wishlist
The Wishlist includes identifications of the Students (Names, Matrikel-Nr. or something like it), identifications of the advanced modules (Names, Number or something like it), the max. number of students which can be assigned to the particular module and the grade which is used to priorities the students. These information have to be saved in a comma separated table formatted as seen in the *exampleTable.pdf* and the *exampleTable.csv*. The following points have to be considered while creating the *.csv* file (Create in a spreadsheet program like EXCLE and then save/export as csv (Comma separated values)).
* Blue Cells (see *example PDF*) must be empty
* Priorities must be integers in the range between 1 and the number of Modules.
* The max. size of Students per module must be an integer.
* The grade must be an integer in the range between 1 and 100
* The Table should only include *ASCII* characters. (e.g. no ä or ß, use ae or ss instead).

### Using the Program
After creating and saving the *Students Wishlist* in *csv* format, you can start the program by double clicking *MAMA.exe* . Click *Browse* and select the created *csv*-File. The path of the file will appear in the upper text field. Click choose to finally select it (The path will appear in green letters in the lower text field.). Finally, click *Start Optimization* to create an assignment for the students. On the right side the graphs should refresh every couple of seconds.

If the assignment is finished a feedback should appear in the lower left text box. If everything went well it should state which percentage the final score is, and that the program finished. If it did not finish without an error correct the students wishlist according to the instructions given in the text box and above. Restart the program and try again.
Once the program has finished, it can be closed

### Interpreting the Results
After the Program successfully finished and has been closed, the assignment can be found in a newly created folder next to the *WISHLIST.csv* . It contains an image of the analysis plots, the original wishlist and the one as interpreted by the program (these should be identical) and the final assignment.

The final assignment is a csv table with can be opened with a spreadsheet program like EXCLE either by simply double clicking or Date/External Data/From Text (might differ from version to version). Alternatively, it can also be read by a simple text editor or online by something like this *http://www.convertcsv.com/csv-viewer-editor.htm*). It contains a table which includes every student and every module. 0 means that the students has not been assigned to this module, a higher number means he has been assigned to it. The value of the number corresponds to the priority the particular student has given this particular module.

## Disclaimer
Always recheck the results for plausibility!!!
Different runs will lead to different assignments. Although they should be very similar regarding the final score, the plot can be checked to choose the best out of several runs on the same *Wishlist*.

## Authors

* **Christoph Neu** - *Initial work* - [kEks](https://github.com/keksundso)
* **Richard Henze** - *Made it proper* - [DonNeoMir](https://github.com/DonNeoMir)

