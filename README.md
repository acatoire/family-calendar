# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/acatoire/family-calendar/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                             |    Stmts |     Miss |   Branch |   BrPart |   Cover |   Missing |
|--------------------------------- | -------: | -------: | -------: | -------: | ------: | --------: |
| app.py                           |      176 |      133 |       40 |        0 |     22% |27, 34-35, 73-127, 131-136, 139-159, 162-166, 171-190, 197-210, 217-233, 238-254, 276-277, 282-326 |
| client\_secret\_env.py           |        3 |        0 |        0 |        0 |    100% |           |
| test\_date\_usage.py             |       22 |        0 |        0 |        0 |    100% |           |
| workdays/\_\_init\_\_.py         |        0 |        0 |        0 |        0 |    100% |           |
| workdays/test\_event\_content.py |       11 |        0 |        0 |        0 |    100% |           |
| workdays/test\_event\_manager.py |       26 |        0 |        0 |        0 |    100% |           |
| workdays/workdays.py             |       29 |        5 |        6 |        2 |     80% |52, 66-67, 87-88 |
|                        **TOTAL** |  **267** |  **138** |   **46** |    **2** | **44%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/acatoire/family-calendar/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/acatoire/family-calendar/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/acatoire/family-calendar/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/acatoire/family-calendar/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Facatoire%2Ffamily-calendar%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/acatoire/family-calendar/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.