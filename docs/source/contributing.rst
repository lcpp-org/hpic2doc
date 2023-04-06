Contributing
============

Organization of work
--------------------

All updates to the code not related to bugs should be directed by the needs of one of the `Projects <https://github.com/lcpp-org/hpic2/projects>`_.
Projects are overarching or ultimate goals for code capabilities.

Work toward a project is subdivided into discrete units using `issues <https://github.com/lcpp-org/hpic2/issues>`_.
Issues are used to track who is doing what work when and why
and allows all developers to follow the progress of work that may be of interest.
It also allows project managers to direct work.
All work done with hpic2, including addressing bugs and preparing papers or conference presentations,
should be tracked with an issue.
There are different types of issues used in hpic2 development that will be described below.

Generally, new features to hpic2 should involve:

#. Implementing the feature.
#. Adding testing for the feature.
#. Documenting the feature in the release notes, the user manual, and (if applicable) the theory manual.

Each of these should have its own issue associated to it, all under the purview of an overarching `multistep <https://github.com/lcpp-org/hpic2/labels/multiple%20steps>`_ issue.
More detail below.

Creating issues
---------------

Creating new issues involves the following steps:

#. Listing appropriate assignees -- usually including yourself.
#. Applying appropriate labels.
#. Listing appropriate project(s).
#. Writing a brief but descriptive title and a less brief and more descriptive summary.

Labels
^^^^^^

There are generally two classes of labels: **type** labels, which describe the type of work that must be performed,
and **status** labels, which determine the working status of the issue.
Each issue should have one of each of these classes applied.

The **type** labels are as follows:


* `bug <https://github.com/lcpp-org/hpic2/labels/bug>`_\ : Code is not behaving as desired and needs to be fixed. Issues with this label do not necessarily need to be attached to any project unless the bug is due to updates for a project.
* `documentation <https://github.com/lcpp-org/hpic2/labels/documentation>`_\ : This issue doesn't involve touching the code, but updating documentation for the code.
* `enhancement <https://github.com/lcpp-org/hpic2/labels/enhancement>`_\ : This issue entails adding new features to the code or supporting recently added features.
* `question <https://github.com/lcpp-org/hpic2/labels/question>`_\ : This issue doesn't involve touching the code, but it opens up a discussion about aspects of the code.
* `task <https://github.com/lcpp-org/hpic2/labels/task>`_\ : This issue may not necessarily involve touching source code, but may involve using the code. Writing papers or using the code for research both fall into this category.

The **status** labels are as follows:


* `working <https://github.com/lcpp-org/hpic2/labels/working>`_\ : Assignees are currently working on this issue.
* `paused <https://github.com/lcpp-org/hpic2/labels/paused>`_\ : Assignees could be working on this issue, but aren't.
* `blocked <https://github.com/lcpp-org/hpic2/labels/blocked>`_\ : Assignees cannot work on this issue. This is usually because work on this issue must wait for another issue to be closed. The issue should have a comment explaining why work is blocked.
* `under review <https://github.com/lcpp-org/hpic2/labels/under%20review>`_\ : Assignees have finished working on this issue and the related pull request is currently being reviewed.
* `multiple steps <https://github.com/lcpp-org/hpic2/labels/multiple%20steps>`_\ : This is an important one, and probably deserves to be its own class rather than listed as a status label. Most feature updates to hpic2 will likely involve the creation of a multistep issue. This is because feature updates involve test and documentation updates in addition to the feature implementation itself. The multistep issue tracks the feature update at large, with individual issues associated with the underlying steps. The multistep issue should list the steps required for completion using checkboxes with Markdown. As issues related to those steps are created, they should be referenced next to the appropriate step checkbox, and as the steps are finished and issues closed, check off the boxes.

Creating issues for a feature addition
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As described above, implementing a new feature often involves testing and documentation updates.
To keep track of the relation between these updates, a developer working on a feature addition should add a multistep issue that describes the new feature, lists the steps required to fully add it, and references the issues associated to each step, ideally using a Markdown checkbox list.
This multistep issue should have both the `multiple steps <https://github.com/lcpp-org/hpic2/labels/multiple%20steps>`_ and `enhancement <https://github.com/lcpp-org/hpic2/labels/enhancement>`_ labels.
The `multiple steps <https://github.com/lcpp-org/hpic2/labels/multiple%20steps>`_ label serves as the status label for this issue.

The first step of a feature addition is to write the feature to the source code.
This should have its own issue, with an `enhancement <https://github.com/lcpp-org/hpic2/labels/enhancement>`_ label and a status label that reflects whether the issue is being worked.
The description should also reference the multistep issue that it supports.
After finishing this work and closing the issue, mark the step as completed in the multistep issue.

If applicable, the second step is to test the feature.
Because writing tests usually involves modifying source code to overcome bugs that come up,
the issue for this step should also have the `enhancement <https://github.com/lcpp-org/hpic2/labels/enhancement>`_ label and a status label that reflects whether the issue is being worked.
The description should also reference the multistep issue that it supports.
After finishing this work and closing the issue, mark the step as completed in the multistep issue.

If applicable, the third step is to update documentation to support the new feature.
By now, the source code ideally does not need to be modified.
The issue for this step should have the `documentation <https://github.com/lcpp-org/hpic2/labels/documentation>`_
label and a status label that reflects whether the issue is being worked.
The description should also reference the multistep issue that it supports.
After finishing this work and closing the issue, mark the step as completed in the multistep issue.

Once all steps are completed, ensure that they are marked as completed in the multistep issue,
and then close it.

Beginning work on an issue
--------------------------


* Add the `working <https://github.com/lcpp-org/hpic2/labels/working>`_ label to the issue.
* Create a feature branch:

  #. Ensure that you have the latest ``main`` by running ``git fetch``\ , followed by ``git checkout main`` and ``git pull``.
  #. Create a new branch locally by running ``git checkout -b <branchName>``.
  #. Push this to the remote by running ``git push -u origin <branchName>``.

* Convention for branch naming is to use the issue number followed by the issue in non-decorated lowercase letters with hyphens replacing spaces. So if issue #42 has name "Add Foo testing," the branch name would be ``42-add-foo-testing``.

Working on an issue
-------------------

* Make small commits as you go, trying to ensure that the code compiles with every commit (unless doing so would require an unusually large commit).
* At any time after the first push to your remote feature branch, you may create a pull request from it:

  #. From the `branches <https://github.com/lcpp-org/hpic2/branches>`_ page, select "New pull request".
  #. If merging this branch into ``main`` should close the issue, use a `closing keyword <https://help.github.com/en/enterprise/2.16/user/github/managing-your-work-on-github/closing-issues-using-keywords>`_ followed by the issue reference in the pull request description. Usually "Closes #\ ``<issueNumber>``\ " suffices.
  #. If the pull request is not yet ready for review, select "Create draft pull request" from the drop-down menu below the description box. Otherwise, select "Create pull request".

* Convention for pull request naming is to use "PR: " followed by the issue name. So if issue #42 has name "Add Foo testing," the pull request name would be "PR: Add Foo testing."
* To integrate updates to ``main`` to your feature branch:

  #. ``git checkout main``
  #. ``git pull``
  #. ``git checkout <branchName>``
  #. ``git merge main``
  #. If conflict issues arise, deal with them.

Sharing work for a review
-------------------------

* Push any local changes to the remote branch with ``git push``.
* Create a pull request if you have not already done so and mark it ready for review.
* Assign reviewer(s) to the pull request.
* Remove the `working <https://github.com/lcpp-org/hpic2/labels/working>`_ label and add the `under review <https://github.com/lcpp-org/hpic2/labels/under%20review>`_ label to the issue.
* Work with your reviewer(s) to make any required changes.
* Ensure that the code compiles without any additional errors or warnings and all tests pass.

Merging approved pull requests
------------------------------


* Integrate the latest updates to ``main``

  #. ``git checkout main``
  #. ``git pull``
  #. ``git checkout <branchName>``
  #. ``git merge main``
  #. ``git push``

* Check one last time that the code compiles without any additional errors or warnings and all tests pass.
* From the `pull request <https://github.com/lcpp-org/hpic2/pulls>`_ page, select your pull request, and select "Squash and merge" from the drop-down menu. You may modify the commit message so that it says exactly what you want it to say in the ``main`` commit history.

Clean up
^^^^^^^^

* Delete the remote branch.
* Delete your local branch with ``git branch -D <branchName>``.
* Ensure that the issue is closed, if applicable.

hpic2 attempts to adopt a uniform code style to promote rapid development and reduce the workload of developers adding features to unfamiliar parts of the codebase. All developers are encouraged to use the following C++ style guide to this end.


Coding conventions
------------------

File organization
^^^^^^^^^^^^^^^^^

Whereas traditional C++ applications split code into headers
containing declarations
and source files containing definitions,
restrictions on linking for some GPU programming models require us to split
code into three files:
a header containing declarations,
with device-enabled function declarations accompanied by the ``KOKKOS_FUNCTION``
decorator;
a source file containing definitions of objects that will only ever
exist on the host;
and a pseudo-source file containing definitions of objects that could be on
device, typically all accompanied by the ``KOKKOS_INLINE_FUNCTION`` decorator.
This pseudo-source file is really a header and is not compiled by itself.
Its purpose is to separate declarations and definitions as is tradition,
but also to provide every translation unit that #includes it
local definitions of device functions,
which is required by some GPU programming models.

An example is as follows.
A class is defined in the header ``Example.hpp``\ , as usual:

.. code-block:: c++

   #ifndef EXAMPLE_HPP
   #define EXAMPLE_HPP

   class Example {
   public:
       void doOutput();

       KOKKOS_FUNCTION
       void doDeviceOutput();
   };

   #include "Example_impl.hpp"

   #endif // Example.hpp

Its host method is defined in the source file ``Example.cpp``\ :

.. code-block:: c++

   #include "Example.hpp"

   void Example::doOutput() { printf("Output from host"); }

Its device method is defined in the pseudo-source file ``Example_impl.hpp``\ :

.. code-block:: c++

   #ifndef EXAMPLE_IMPL_HPP
   #define EXAMPLE_IMPL_HPP

   KOKKOS_INLINE_FUNCTION
   void Example::doDeviceOutput() { printf("Output from device"); }

   #endif EXAMPLE_IMPL_HPP

Since the device pseudo-source is still potentially 
included in translation units,
we give it header guards.
However, note that at the end of ``Example.hpp``\ ,
we ``#include "Example_impl.hpp"``.
This ensures that all translation units that ``#include "Example.hpp"``
get definitions of the device functions in the absence of relocatable device code.
Mostly, this is so that headers act as a C++ programmer with no GPU
programming experience would expect.

In some cases, the definitions in the pseudo-source file will
never be used in a translation unit,
so the compile time for that translation unit is unnecessarily inflated.
Our to convention to sidestep circumvent this is to wrap its #include
at the end of ``Example.hpp`` as follows:

.. code-block:: c++

   #ifndef HPIC2_NO_DEVICE_FUNCTIONS
   #include "Example_impl.hpp"
   #endif // HPIC2_NO_DEVICE_FUNCTIONS

A translation unit need only ``#define HPIC2_NO_DEVICE_FUNCTIONS`` locally
somewhere before its #includes
to avoid the expense of compiling device code it will never use.

Entity naming
^^^^^^^^^^^^^

In general, the more descriptive the name, the better.
Since this isn't F77, don't feel that you have to abbreviate every variable name.
Staying within 80 columns looks nice, but cutting names of complicated entities short to fit inside 80 columns can do more harm than good.

Classes and structs should be named in **PascalCase**\ , as follows:

.. code-block:: c++

   class SomeImportantClass {}

Functions should be named in **camelCase**\ ;
protected and private class methods should also have a trailing underscore.

.. code-block:: c++

   void printImportantInfo() {}

   class SomeImportantClass {
     protected:
       void printClassStuff_() {}
   }

Variables should be named in **snake_case**\ ;
protected and private class member variables should also have a trailing underscore.

.. code-block:: c++

   double some_important_variable;

   class SomeImportantClass {
     private:
       int another_important_variable_;
   }

Includes formatting
^^^^^^^^^^^^^^^^^^^

List local includes first, with the file format and inside quotation marks.
List dependency includes second, with the file format and inside angled brackets.
List system includes last, with no file format and inside angled brackets:

.. code-block:: c++

   #include "hpic_namespace.hpp"
   #include <toml.hpp>
   #include <iostream>

MPI
^^^

For compatibility with the user-level failure mitigation extension to MPI,
collective calls that would normally use the ``MPI_COMM_WORLD`` communicator should
instead use the centralized ``MPIHandler::main_comm`` communicator.
In addition, the ID of the main rank can be obtained through ``MPIHandler::main_rank``\ ,
and ``MPIHandler::is_main`` is a boolean that can be used to determine whether the calling rank is the main rank.
Developers desiring to use finer-grained communicators should consult with project owners.


Contributor Covenant Code of Conduct
------------------------------------

Our Pledge
^^^^^^^^^^

We as members, contributors, and leaders pledge to make participation in our
community a harassment-free experience for everyone, regardless of age, body
size, visible or invisible disability, ethnicity, sex characteristics, gender
identity and expression, level of experience, education, socio-economic status,
nationality, personal appearance, race, religion, or sexual identity
and orientation.

We pledge to act and interact in ways that contribute to an open, welcoming,
diverse, inclusive, and healthy community.

Our Standards
^^^^^^^^^^^^^

Examples of behavior that contributes to a positive environment for our
community include:


* Demonstrating empathy and kindness toward other people
* Being respectful of differing opinions, viewpoints, and experiences
* Giving and gracefully accepting constructive feedback
* Accepting responsibility and apologizing to those affected by our mistakes,
  and learning from the experience
* Focusing on what is best not just for us as individuals, but for the
  overall community

Examples of unacceptable behavior include:


* The use of sexualized language or imagery, and sexual attention or
  advances of any kind
* Trolling, insulting or derogatory comments, and personal or political attacks
* Public or private harassment
* Publishing others' private information, such as a physical or email
  address, without their explicit permission
* Other conduct which could reasonably be considered inappropriate in a
  professional setting

Enforcement Responsibilities
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Community leaders are responsible for clarifying and enforcing our standards of
acceptable behavior and will take appropriate and fair corrective action in
response to any behavior that they deem inappropriate, threatening, offensive,
or harmful.

Community leaders have the right and responsibility to remove, edit, or reject
comments, commits, code, wiki edits, issues, and other contributions that are
not aligned to this Code of Conduct, and will communicate reasons for moderation
decisions when appropriate.

Scope
^^^^^

This Code of Conduct applies within all community spaces, and also applies when
an individual is officially representing the community in public spaces.
Examples of representing our community include using an official e-mail address,
posting via an official social media account, or acting as an appointed
representative at an online or offline event.

Enforcement
^^^^^^^^^^^

Instances of abusive, harassing, or otherwise unacceptable behavior may be
reported to the community leaders responsible for enforcement at
the LCPP Slack.
All complaints will be reviewed and investigated promptly and fairly.

All community leaders are obligated to respect the privacy and security of the
reporter of any incident.

Enforcement Guidelines
^^^^^^^^^^^^^^^^^^^^^^

Community leaders will follow these Community Impact Guidelines in determining
the consequences for any action they deem in violation of this Code of Conduct:

1. Correction
"""""""""""""

**Community Impact**\ : Use of inappropriate language or other behavior deemed
unprofessional or unwelcome in the community.

**Consequence**\ : A private, written warning from community leaders, providing
clarity around the nature of the violation and an explanation of why the
behavior was inappropriate. A public apology may be requested.

2. Warning
"""""""""""

**Community Impact**\ : A violation through a single incident or series
of actions.

**Consequence**\ : A warning with consequences for continued behavior. No
interaction with the people involved, including unsolicited interaction with
those enforcing the Code of Conduct, for a specified period of time. This
includes avoiding interactions in community spaces as well as external channels
like social media. Violating these terms may lead to a temporary or
permanent ban.

3. Temporary Ban
""""""""""""""""

**Community Impact**\ : A serious violation of community standards, including
sustained inappropriate behavior.

**Consequence**\ : A temporary ban from any sort of interaction or public
communication with the community for a specified period of time. No public or
private interaction with the people involved, including unsolicited interaction
with those enforcing the Code of Conduct, is allowed during this period.
Violating these terms may lead to a permanent ban.

4. Permanent Ban
""""""""""""""""

**Community Impact**\ : Demonstrating a pattern of violation of community
standards, including sustained inappropriate behavior,  harassment of an
individual, or aggression toward or disparagement of classes of individuals.

**Consequence**\ : A permanent ban from any sort of public interaction within
the community.

Attribution
^^^^^^^^^^^

This Contributor Covenant Code of Conduct is adapted from the `Contributor Covenant <https://www.contributor-covenant.org>`_\ ,
version 2.0, available at
https://www.contributor-covenant.org/version/2/0/code_of_conduct.html.

Community Impact Guidelines were inspired by `Mozilla's code of conduct
enforcement ladder <https://github.com/mozilla/diversity>`_.

For answers to common questions about this code of conduct, see the FAQ at
https://www.contributor-covenant.org/faq. Translations are available at
https://www.contributor-covenant.org/translations.
