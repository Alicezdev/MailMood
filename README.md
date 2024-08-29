<p align="center">
  <img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" alt="project-logo">
</p>
<p align="center">
    <h1 align="center">MAILMOOD</h1>
</p>
<p align="center">
    <em><code>► INSERT-TEXT-HERE</code></em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/Alicezdev/MailMood?style=default&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/Alicezdev/MailMood?style=default&logo=git&logoColor=white&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Alicezdev/MailMood?style=default&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Alicezdev/MailMood?style=default&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Modules](#-modules)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Project Roadmap](#-project-roadmap)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

##  Overview

<code>► MailMood is a tool to detect the emotion behind your emails using the rule-based sentiment analysis tool.</code>

---

##  Features

<code>► Detect Email Emotion with a Simple UI</code>

---

##  Repository Structure

```sh
└── MailMood/
    ├── MailMood-backend
    │   └── MailMood.py
    └── MailMood-frontend
        ├── index.html
        ├── script.js
        └── style.css
```

---

##  Modules

<details closed><summary>MailMood-backend</summary>

| File                                                                                          | Summary                         |
| ---                                                                                           | ---                             |
| [MailMood.py](https://github.com/Alicezdev/MailMood/blob/master/MailMood-backend/MailMood.py) | <code>► flask flask_cors nylas vaderSentiment</code> |

</details>

<details closed><summary>MailMood-frontend</summary>

| File                                                                                         | Summary                         |
| ---                                                                                          | ---                             |
| [index.html](https://github.com/Alicezdev/MailMood/blob/master/MailMood-frontend/index.html) | <code>► jQuery, Slick Carousel Chart.js</code> |
| [script.js](https://github.com/Alicezdev/MailMood/blob/master/MailMood-frontend/script.js)   | <code>► </code> |
| [style.css](https://github.com/Alicezdev/MailMood/blob/master/MailMood-frontend/style.css)   | <code>► </code> |

</details>

---

##  Getting Started

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the MailMood repository:
>
> ```console
> $ git clone https://github.com/Alicezdev/MailMood
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd MailMood/MailMood-backend
> $ touch .env
> $ nano .env
> ```
> 3. Add below enviroment variable
> ```console
> NYLAS_API_URI=https://api.us.nylas.com
> NYLAS_GRANT_ID=<YOR EMAIL GRANT ID>
> NYLAS_ACCESS_TOKEN=<YOR EMAIL ACCESS TOKEN>
> ```

<h4>Using <code>pip</code></h4>

> ```console
> $ pip install flask
> $ pip install flask-cors
> $ pip install python-dotenv
> $ pip install logging
> $ pip install nylas
> $ pip install vaderSentiment
> ```




###  Usage

<h4>Using <code>Python3</code></h4>

> Run MailMood using the command below:
> ```console
> $ > python3 MoodMail.py
> ```
> Open index.html in your browser and enter the email

---

##  License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

##  Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-overview)

---
