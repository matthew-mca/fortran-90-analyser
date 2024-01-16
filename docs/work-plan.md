# Updated Problem Description, Solution Approach and Work Plan

After the creation of the first digital computer back in 1945, computer scientists were able to
interact with the underlying hardware of such machines by writing assembly language programs, a
language which bore a strong resemblance to the machine code instructions of the hardware itself.
This was a great innovation in the field of computer science, but it presented a problem - in order
to interact with digital computers in this way, any users were required to have a deep knowledge of
the underlying machinery and assembly language, which presented a barrier for entry into the
profession.

Touted as one of the first high-level programming languages, FORTRAN (FORmula TRANslator) was
invented in 1954 at IBM by John Backus. Its main use case was in scientific and engineering
applications, where to this day it remains a popular choice due to the myriad of mathematical
functions available in the language, as well as its efficiency compared to modern languages.

FORTRAN has gone under many revisions, with the most recent version being released in November of
2023. However, this project will be looking at Fortran 90, released in 1991. Due to both its age and
nature as a niche programming language, there are not many reliable tools readily available for use
with Fortran 90.

This project aims to create a tool which can analyse Fortran 90 code and report metrics back to the
user about their code, such as the number of variables used, functions called, etc. The analyser
will be able to take input from the user about the location of their codebase (local path, online,
etc) and will parse the code in its entirety. After this, the analyser can then present metrics to
the user, as well as storing the results to a database where earlier scans can be viewed and
compared to more recent versions of the code.

## Solution Approach

In order to deduce the steps the analyser should take in order to parse and report on the code, it
is useful to look at this from the end result and work backwards:

- *I would like to be able to view metrics on my present and past Fortran 90 code, so*
- *I will need to be able to retrieve past results from a database, and*
- *I will need to be able to accurately identify the smallest parts of my code e.g. variables,*
  *function calls, etc. so*
- *I will need to be able to accurately identify the larger parts of my code, such as programs,*
  *modules, and derived types, so*
- *I will need to be able to read the contents of Fortran files, so*
- *I will need to figure out what files in a codebase are Fortran 90 files and where they are, so*
- *I will need to be able to traverse a directory provided to me by a user, so*
- *I will need to be able to accept input from the user about the location of the codebase.*

I will look at the above steps from start to end, to follow the logical progression of the analyser
as it is developed.

### Accepting Input from the User

The first step in order to begin parsing a Fortran codebase is to figure out where the codebase is.
Is the codebase on the user’s local machine? Is the codebase hosted in a GitHub/GitLab repository?
The analyser will need to know where to look via input from the user.

The first, and most likely starting point for taking input from the user is a Command Line Interface
(CLI) that is included as part of the application. While it is not as user friendly as a GUI, it is
a good starting point for accepting user input and provides us with an entry point into the
application. Since the overall analyser is being written in Python, there are libraries available
for use that assist in the building of a CLI.

One such CLI library is the library Click, which is quoted on its website as “a Python package for
creating beautiful command line interfaces in a composable way with as little code as necessary.”
The advantage of this library is that I have actually used this in a production codebase during my
placement year at Rapid7, meaning that I already have pre-existing knowledge of this library and
know that it has enough features to suit my use case in this project.

When enough functionality is in place and there is a suitable amount of features available to the
user via the CLI, if time permits I would like to look into creating a GUI for the application. A
GUI would allow for a more user-friendly experience when using the application, since rather than
having to consult documentation and configure user inputs on the command line, the user can simply
click on icons and windows to navigate between the different parts of the application, can configure
the analyser’s options in a simpler manner, and can also receive richer metrics about the code
through visualisations in the GUI.

### Codebase Traversal and File Discovery

Once the location of the codebase has been established, the next step is to traverse the codebase
and find out the overall directory structure, e.g. folder and file names, which files are Fortan 90
files, where in the codebase these Fortran files are located, etc.

The best approach here is to create some sort of logic that is solely responsible for reading
directories and files, which will start from the root of the codebase and visit every directory and
scan its contents. These contents can then be checked to see if they are a Fortran 90 file, another
type of digital file, or a sub-folder within the current folder.

Since we are only really interested in the Fortran 90 files in the codebase, it is likely we will
have 2 types of classes/objects for representing files: one for Fortran 90 files, and another for
everything else. Upon visiting any Fortran 90 files, we can create a slightly more sophisticated
representation of the file that will contain more information than any other type of file (more on
this in the “Reading Fortran 90 File Contents” section). Once all objects contained within the
codebase have been detected and parsed, we can return the result to the CLI, which will gather the
appropriate metrics from the result and present them to the user.

### Reading Fortran 90 File Contents

Upon encountering a Fortran 90 file, before any analysis can begin, we must first extract the
contents of the file. Luckily, Python’s file reading functionality is very capable of handling the
reading of text-based files. Once we have established a connection to the file in the code, Python
allows for reading of individual lines in the file one after another.

Since we do not know the size of any potential Fortran 90 files that we will encounter, the best
approach here will likely be to create a function that “yields” the file contents rather than
returning it. When a function uses the yield keyword rather than return, the function returns a
generator object (as opposed to a list of lines in the case of reading lines in a file). Generator
objects are more memory-efficient than returning the entire result at once, as generators are known
as “lazy iterators”. This means that the next result in the generator is computed until it is asked
for, which saves storing the entire contents of a file to memory. This will be beneficial to our use
case, as extremely massive Fortran 90 files could cause our file reading logic to fail if we were to
try and store the entire contents of the file to memory.

### Identifying Program Units

With the contents of our Fortran file read, the next step will be to begin looking at the contents
closer and start to pick out points of interest in the code. The first such step is to find where
the different program units start and end. Like many other programming languages, there are
conventions attached to Fortran 90 that dictate every module/program should be housed in its own
file, but as part of making the analyser robust we will build the logic in such a way that we can
parse any and all program units in a file.

In order to understand the types of code blocks we will want to parse, we will need to know what
they are and how to declare them in the code. For the most part, declaring functions, programs,
modules etc. in Fortran 90 requires a statement to declare the start of the block, and a statement
to declare its end. Research will need to be conducted into the syntax of Fortran 90 to understand
all the different types of blocks available in Fortran, as well as what their starting and end
statements look like.

When research is finished, the patterns should be implemented into the analyser in such a way that
they can then be used when reading the contents of a Fortran 90 file, where they can be compared to
each line in the file to see if the line is a potential start/end statement for a certain type of
block. The best way I can think of to accomplish this is through the use of a regex pattern, one for
each type of statement we want to find. This means that for each unique type of program unit, there
will likely be 2 regex patterns for it: one for its start, and one for its end.

### Identifying Variables, Function Calls, etc

With program units now detected by the analyser, we can drill down deeper into each unit and read
the variables, function calls, and other key parts of the unit. A likely feature at this level will
be finding out the scope/usage of any detected variables or functions, i.e. is a variable scoped
locally to the function we found it in? Is it a global variable taken from another part of the file?
What file is the function we are calling implemented in? We will need a way to establish
relationships between these “smaller parts” of the code that can reliably find where such parts are
used across the codebase, since program units like functions are commonly imported into other files
for use. It would be beneficial to know how far across the codebase components like this actually
reach.

### Storing/Retrieving Analysis Results using Persistent Storage

When parsing is complete, we not only want to present the current results to the user, but store
these results away so that they can be accessed in later sessions. The ability to access previous
scans of the codebase also means we could incorporate “diffing” logic (think Git when modifying the
contents of a file) where we can show the changes in variable counts, number of program units, etc.
per file. Much like other applications that store files, another useful feature here would be to
allow for exporting of previous scans, for example into a CSV file or report document for compliance
purposes.

Since this analyser is smaller-scale than an enterprise-grade application and is also not sharing
the underlying database with any other software, an SQLite database would be the most appropriate
storage solution for this analyser. This will allow for a more lightweight storage solution that
still allows us to establish relationships and use SQL for querying our data. A package such as the
SQL toolkit “SQLAlchemy” can be added to the analyser at this point to allow us to use Python when
coding the logic for the database and reduce the complexity of this step.

### Reporting/Comparing Metrics

Reporting metrics back to the user is the focal point of the application. This can be either through
a scan conducted on the code by the analyser, or through retrieving an older scan from storage for
review.

While only using a CLI, we are limited with how far reporting our metrics can go. While we can still
compute metrics, we are limited to displaying output in the terminal or exporting a file with our
results to an external folder, such as a report or chart. With a GUI, we can present such
visualisations/reports directly to the user in real time, and give them the option to do with it as
they see fit. Using the likes of charts in a GUI also means that mass amounts of data can be
condensed into one or more such charts to make it easier to view at a glance.

### Bonus: Implementing Engineering Best Practices

Since this project is very development-heavy, steps will need to be taken to ensure that the code
written as kept consistent, well documented, and tested thoroughly.

In order to ensure correctness of code, testing will need to be added for most (if not all) of the
project. Unit tests should test the correctness of individual classes/functions, but integration
tests should also be added. There are many codebases on sites like GitHub that host Fortran 90
repositories free for others to use as they need. Some of these repositories could be added into the
project as live data for use in any integration tests.

Beyond code correctness, tools such as the code formatter Black, the type checker Mypy, the linter
flake8, etc. can be used to ensure that the code is kept high quality and consistently formatted.
These tools can also be used with pre-commit hooks and CI pipelines to check that formatting is
correct, ensuring that a high standard is kept on every commit and every merge request. This also
takes the pressure off trying to manually keep track of formatting and allows a developer to focus
fully on making sure the underlying logic makes sense.

## Work Plan

For ALL work in the project, every single piece of work committed to the analyser’s repository will
be done on a separate branch, each with their own accompanying issue and merge request. This avoids
committing any changes directly to the main branch, a common practice in a project with branching
workloads. The use of issues and merge requests also allows for tracking of issues even after they
are merged and closed.

There is a README at the root of the project which will be updated throughout the project that will
house information about the project. This means that relevant information can be found within the
repository, meaning that any supervisors for this project do not have to wait until the dissertation
deadline in order to access written information about the project.

I am going to separate the development of the analyser into distinct phases, each with a set of
system requirements for the project at this point. These phases will take a similar layout (but not
1:1!) to the above sections of the solution approach:

### Create Entry Point into Application

- *The system should have a CLI which the user can call while supplying the path of a*
  *file/directory.*
- *There should be at least one command that can verify the pathing logic in the application works*
  *correctly.*

### Creating File/Directory Representations

- *Three classes should exist within the application: a class for representing directories, and two*
  *classes for representing files.*
- *One of the file classes should represent a simple digital file; the other class should represent*
  *a Fortran 90 file.*
- *The Fortran 90 file class should extend the simple file class.*
- *There should be a part of the Fortran 90 file class for storing/retrieving a collection of lines*
  *that make up a Fortran 90 file.*

### Reading Fortran 90 File Contents

- *There should be a parser created responsible for traversing a given directory and distinguishing*
  *Fortran 90 files from directories and non-Fortran files.*
- *This parser should be able to extract the contents of any Fortran file it finds and use it to*
  *create an object.*

### Identifying Program Units

- *The system should not only be able to read the contents of Fortran files, but should be able to*
  *reliably and accurately distinguish the start and end of distinct program units.*

### Identifying Variables, Function Calls, etc

- *The system should be able to analyse the inner contents of code blocks and record any variables,*
  *comments, functions, etc. that it finds.*
- *The system should be able to differentiate variables at different scopes, e.g. if two occurrences*
  *of a variable are the same or if they are simply two local variables with the same name.*
- *The system should be able to store the scope of any variables/functions as part of its*
  *representation.*
- *The system should be able to find if a given function is imported into any other files (and where*
  *in the other file it is called).*

### Storing/Retrieving Analysis Results

- *There should be a database added to the application that can store the results of a codebase*
  *scan.*
- *There should be a way to uniquely identify which codebase a scan result belongs to so that the*
  *history of scans on a given codebase does not unintentionally include scan data from a different*
  *codebase.*

### Reporting/Comparing Metrics

- *The system should be able to take input from the user about what metrics to report back on scan,*
  *and which to ignore (ALL data should still be saved to persistent storage).*
- *The system should be able to export older scans as well as the current scan. This could be in the*
  *form of a CSV, html file, etc.*

### Creating GUI

- *The system should have an interactive UI for the user to interact with.*
- *The UI should make API calls to the backend when attempting to populate the UI with data.*
- *There should be options to visualise present/past data in the form of charts.*