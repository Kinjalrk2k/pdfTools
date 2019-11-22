# pdfTools
A small CLI python script based on PyPDF2 for extracting, merging and doing a lot more on pdf files

### Usage
* Clone this repository
* Browse the cloned location
* Install dependencies: ````pip install -r requirements.txt````
* Run the python script. Read more detials below!

### Running the script
Basic syntax:
````py pdftools.py -d <directory> -e "<expression>" -o <output file> --nb````

Following are the command line options and details on arguments:

| Option                   | Priority   | Description                                                                                                                        | Default behaviour                                                   |
|--------------------------|------------|------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------|
| ````-d <directory>````   | Optional   | use ````-d```` followed by the directory in which the pdf files are stored. *(use "" if the path to directory contains spaces)*    | Use the directory where the script ````pdftools.py```` is located   |
| ````-e <expression>````  | Optional   | use ````-e```` followed by a expression to slice and merge files. It is mandatory to use "". *(Read more about expression below!)* | Use all the .pdf files available in the directory to merge fully    |
| ````-o <output file>```` | Optional | use ````-o```` followed by the name (or full path) of the output file. *(use "" if the path to directory contains spaces)*         | Generates ````output.pdf```` file in the directory as output file                                                                |
| --nb                     | Optional   | use ````--nb```` for disabling the auto bookmarking at the merge points                                                            | Puts up bookmarks in the merge points with the respective filenames |
| -h                       | Optional   | opens a help prompt                                                                                                                | N/A                                                                 |

### Writing the expression
#### Page numbers start form 0 (zero-indexed)
* Use exact filenames
* Use ````[:]```` notation to extract files - Same as python slicing
  * ````[x:y]```` will extract pages x to y-1
  * ````[:y]```` will extract pages 0 to y-1
  * ````[x:]```` will extract pages x to the end of the document
  * ````[:]```` will extract the whole document - in other words: no extraction, use the full document
  *(Note: It is mandatory to use this when you want the whole document. Skipping this would lead to uncaught exceptions)*
* Use ````+```` to merge files

Example: ````"abc.pdf[1:3] + def.pdf[:10] + ghi.pdf[7:] + jkl.pdf[:]"````

### Dependencies
[Click here](https://github.com/Kinjalrk2k/pdfTools/network/dependencies) to explore the dependency graph.

| Dependency | Version |
|------------|---------|
| ```PyPDF2```       | 1.26.0   |

### Notes
This project was created and tested under Windows, and is expected to work fully in other systems too.

This project is still under development. Parts of the source codes may not be well documented.
Also suitable prompts may not be available for the user at the moment.

More features and fixes are yet to come. Meanwhile suggestions, ideas, bug reports are welcomed.

I am a python n00bie! I am still learning python! I have tried my best to give in as much effort required (of course directly proportionate to my knowledge), for this project.

<br>***Kinjal Raykarmakar***
