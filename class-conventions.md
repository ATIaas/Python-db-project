# Reference for OOP practices and schemas.
---
## ***WHY*** use classes.

#### Using __classes__ has some key benefits.

1. Ease of testing.
   -  We can better organize our unitary testing suites based on classes for more comprehensive unitary test script naming schemes.
     
   -  For integration and functionality testing, the use of ***dummy** classes with hardcoded expected results, will help with closing the scope of the tests in the desired section.
  
   -  Use of classes leads to more organized and compact end-to-end, acceptance and post acceptance testing, due to inherit modularity.
     
2. Usability and cooperation, by having all functions associated with a certain part of the functionality.
   - By creating a mockup of the class with the return types and expected results associated with its functionality we can start development of functions requiring that functionality before finishing implementation.
  
   - Navigation of class functions inside of an IDE allows us to center in the base functions associated with its scope, via the in class functions, and by the typed function arguments.

3. Inheritance and *build on* mentality.
   - Due to the innate compartmentalization associated with clases, it is easier to maintain a less chaotic code base by having clear limitations associated with the scope of variable access.
  
   - Inheritance allows us to lessen the issues of branch merging and provides us with a framework on how to manage new requirements, without breaking pre-existing code.

---
## ***When to use Classes***

### Rule of thumb is that if one or more of these allies a new class or ***extension of an existing one*** is a good idea.
-  The Functionality has more than ***2-3 abstract steps***.
   + For example Consolidation of the database:
      1. Read the existing file
      2. remove redundant steps
      3. rewrite the file
  
- The functionality has high complexity associated with it that may be better to test in chunks.
    + async file reading chunk by chunk, would have to check.
        1. no chunk is checked more than once.
        2. That the end of a chunk k is paired with the start of the chunk k + 1.
        3. that a chunk that has no line breaks will not be sent to parse without first getting the start of the next chunk and beggining of the one before, __recursively__.
        4. That there are no deadlocks in waiting the next line.
        5. That an empty line will not be sent to parse.
        6. Critical section is correctly assigned.

- ***The functionality builds upon an existing class***
    + ***Just do it in a daughter class or inside the class itself***.
    + ***Don't ruin the scope container***, unless absolutely needed.



---
## Class declarations and naming.

#### It is important that our naming conventions for classes are properly structured to prevent future **misunderstandings**.
---

### ***Class Naming*** conventions.
---
For this purpose some ground rules will be set.

1. Class Names will not start with uppercase letters
   - They are used for key word highlights or camel case

3. Class Names will not contain underscores.

4. Class Names should describe the root purpose of inception.
   - Simple, no one wants to read the odyssey when selecting the class to assign for a variable.

#### Examples

| Right | Wrong |
| ------ | ------ |
| loadedDB | VirtualDB |
| useractionDBhandler | db_user_petition_handler |
| utf32FileHashDB | fileHashDBParserStandardUTF32 |

---

### ***Class Suffixing***.
---
#### What are suffixes for.

Suffixes is a class code that associates the daughter class to its parent class.

#### className__(Parent class suffix).

Suffixes will be used to label daughter classes that can completely replace their parent class like.
-  Standins.
-  Dummies.
-  Alternative versions.

##### for example a testing dummy class for the class with suffix EXTM, will look something like this.
"dummy__EXTM"
or
"dummy__EXTM_unitTST2".


#### Each base class created should have a 3-5 alphanumeric Code to associate it for inheritance purposes with some rules.

1. The Suffix, must be unique --(Don't know how we are going to do that yet)--.
2. The Suffix must describe the class name/ purpose.
3. The Suffix has to be commented in the class description.

___Example___
-  For a class named loadedDB the suffix ROL will not fit meanwhile LDB fits it well.
---

## **Function naming scheme**.
---

## ***For all that is holy in this world, use the norma function naming scheme inside classes***

For simplicity we are going to have 3 scopes of functions.
1. Private.
2. Restricted.
3. Public.

### Private functions.

> That are innate to python and will start with two underscores.
> Example: "__foo()".

We are going to use them accordingly, a private function is usually:
- A sub function called from a main function.
  
- A function that is a common action in the scope.
  
- A section of a functionality that is complex enough or has caused enough trouble to have its own unit test, same as the first basically.

### Restricted function.

> Not inane to python therefore just a naming convention of starting with one underscore.
> Example: "_funcA()".

They will be used to provide interlayer calls and functionality:
-  Functions for between class interaction.
    + Python has no friend class.

-  Functions for troubleshooting/testing purposes that aren't part of the normal functionality.

-  Pre completed implementation coding area in joint branches.
    + If two are working in one branch the main call should stay static till the implementation passes at least the manual testing.

### Public functions.

> They will be used for outward facing functionality, and will have no prefixes.
> Example:"somefuncX()".

Public functions are used for:
-  Outward facing functions, aka client layer calls.
  
-  End result returns for internal functions.
  
-  That's it, ***If in doubt make it restricted first***

  






