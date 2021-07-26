# Warnings-dropoff-analysis

Repository which contains the scripts to retrive user warnings metrics from a MongoDB database.

The collections should be obtained merging the outcomes of [user-metrics](https://github.com/WikiCommunityHealth/user-metrics) and [Wikidump](https://github.com/samuelebortolotti/wikidump) repository.

## Setup

Clone this repository

```bash
git clone https://github.com/WikiCommunityHealth/warnings-dropoff-analysis.git
```

Create the poetry project virtual environment using your current Python version

```bash
make env
```

Install the required packages and dependencies

```bash
make install
```

## Usage

Only after having installed the dependencies in the poetry virtual environment, can you run the following command

```bash
poetry run python -m warnings_dropoff_analysis db-name collection-name [--output-compression gzip] extract-user-warnings-metrics [month to consider the drop-off]
```

Or you can simply edit the `Makefile` and type

```bash
make run
```

The result will be found in the `ouput` folder.

## Plots

After the data has been retrieved, you can plot some basic statistics by typing

```bash
poetry run python plotter/[plotter-stats-file].py [community-lang]
```

Or, as in the previous case, you can edit the `Makefile` and run

```bash
make plot
```

The produced figures can be found in the `plots` folder.

## Note

The script tries, by default, to connect to the local MongoDB instance. 

So as to connect it to a remote one, you can add a  `.env ` file writing the connection string within, following the  `.env.example` template file:

```bash
echo '[your mongodb connection string]' > .env
```

### Note about the chart scripts

Be careful with the plot scripts, since `pandas` memory overhead, to instantiate the DataFrame structure, is extremely RAM consuming.

As a result, make sure you have enough free memory before running one of those scripts.

## Data format

The data retrived by the script is in the following format:

```json
{
  "name": "<name>",
  "id": 21,
  "last_edit_month": 2,
  "last_edit_year": 2010,
  "retirement_declared": false,
  "retire_date": null,
  "retirement_parameters": null,
  "retirement_template_name": null,
  "edit_count_after_retirement": null,
  "last_serious_warning": {
    "name": "avvisoimmagine2",
    "date": "200_-0_-1_ 2_:1_:4_+00:00"
  },
  "last_serious_warning_name": "avvisoimmagine2",
  "last_serious_warning_date": "200_-0_-1_ 2_:1_:4_+00:00",
  "last_normal_warning": {
    "date": null,
    "name": null
  },
  "last_normal_warning_name": null,
  "last_normal_warning_date": null,
  "last_not_serious_warning": {
    "date": null,
    "name": null
  },
  "last_not_serious_warning_name": null,
  "last_not_serious_warning_date": null,
  "average_edit_count_before_last_serious_warning_date": 9.333333333333334,
  "average_edit_count_before_last_normal_warning_date": 0,
  "average_edit_count_before_last_not_serious_warning_date": 0,
  "average_edit_count_after_last_serious_warning_date": 0.0036443148688046646,
  "average_edit_count_after_last_normal_warning_date": 0,
  "average_edit_count_after_last_not_serious_warning_date": 0,
  "count_serious_templates_transcluded": 1,
  "count_warning_templates_transcluded": 0,
  "count_not_serious_templates_transcluded": 0,
  "count_serious_templates_substituted": 0,
  "count_warning_templates_substituted": 0,
  "count_not_serious_templates_substituted": 0,
  "edit_history": {
    "2001": {
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 0,
      "5": 0,
      "6": 0,
      "7": 0,
      "8": 1,
      "9": 0,
      "10": 0,
      "11": 0,
      "12": 0
    },
    "2015": {
      "1": 0,
      "2": 0,
      "3": 0,
      "4": 0,
      "5": 0,
      "6": 0,
      "7": 0,
      "8": 0,
      "9": 0,
      "10": 0,
      "11": 0,
      "12": 3
    }
  },
  "warnings_history": {
    "2005": {
      "10": {
        "serious_substituted": 0,
        "not_serious_substituted": 0,
        "not_serious_transcluded": 0,
        "warning_substituted": 0,
        "warning_transcluded": 0,
        "serious_transcluded": 1
      },
    "2021": {
      "1": {
        "serious_substituted": 0,
        "not_serious_substituted": 0,
        "not_serious_transcluded": 0,
        "warning_substituted": 0,
        "warning_transcluded": 0,
        "serious_transcluded": 0
      },
      "12": {
        "serious_substituted": 0,
        "not_serious_substituted": 0,
        "not_serious_transcluded": 0,
        "warning_substituted": 0,
        "warning_transcluded": 0,
        "serious_transcluded": 0
      }
    }
  },
  "sex": null, 
  "banned": false
}
```

### Fields

A brief description of the fields

- `name` name of the user
- `id` user id
- `last_edit_month` month of the last edit date
- `last_edit_year` year of the last edit date
- `retirement_declared` is a boolean field representing, whether the user has specified a retirement template or not, on the user page or user talk page
- `retire_date` the retirement date if specified
- `retirement_parameters`: parameters specified in the retired template
- `retirement_template_name`: name of the retired template
- `edit_count_after_retirement`: activity count after the retirement date
- `last_serious_warning`: last transcluded serious warning
- `last_serious_warning_name`: the name of the last high severity warning received
- `last_serious_warning_date`: the date of the last high severity warning received
- `last_normal_warning` last transcluded warning of medium severity
- `last_normal_warning_name`: the name of the last medium severity warning received
- `last_normal_warning_date`: the date of the last medium severity warning received
- `last_not_serious_warning` last transcluded non serious warning
- `last_not_serious_warning_name`: the name of the last low severity warning received
- `last_not_serious_warning_date`: the date of the last low severity warning received
- `average_edit_count_before_last_serious_warning_date` average count of actions the user has made before the last serious warning date (in the range of [date - 12 months, date])
- `average_edit_count_before_last_normal_warning_date` average count of actions the user has made before the last warning date (in the range of [date - 12 months, date])
- `average_edit_count_before_last_not_serious_warning_date` average count of action the user has made before the last not serious warning date (in the range of [date - 12 months])
- `average_edit_count_after_last_serious_warning_date` average count of action the user has made after the last serious warning date (in the range of [date, date + 12 months])
- `average_edit_count_after_last_normal_warning_date` average count of action the user has made after the last warning date (in the range of [date, date + 12 months])
- `average_edit_count_after_last_not_serious_warning_date` average count of action the user has made after the last not serious warning date (in the range of [date, date + 12 months])
- `count_serious_templates_transcluded` count of the transcluded serious warnings templates
- `count_warning_templates_transcluded` count of the transcluded warnings templates
- `count_not_serious_templates_transcluded` count of the transcluded not serious warnings templates
- `count_serious_templates_substituted` count of the substituted serious warnings templates
- `count_warning_templates_substituted` count of the substituted warnings templates
- `count_not_serious_templates_substituted` count of the substituted not serious warnings templates
- `edit_history` history of the user's activity per month
- `warnings_history`  history of the user's warnings per month
- `sex`: the user's sex if specified
- `banned`: whether the user is banned or not

## Code documentation

In order to get the code documentation, you can use [pdoc](https://github.com/pdoc3/pdoc) by typing

```bash
make doc
```

Or you can open it directly with your browser using `xdg-open`

```bash
make openDoc
```

## Charts

Here, the plots, produced by the scripts stored in the `plotter` folder, are listed 

### Users who have declared their withdraw from Wikipedia

#### The outcomes of the `retired_stats.py`.

Considering only the users who have declared their withdrawal from Wikipedia:

* A bar chart which indicates the percentage of users who have stopped editing in Wikipedia, and the percentage of users who have continued to be active.
* A bar chart which shows the number of edits the users have made after having declared their withdrawal.
* A bar chart which illustrates the percentage of men and women who have declared the withdrawal from Wikipedia

### Users who have received at least a warning of medium severity

#### The outcomes of the `serious_warnings_stats.py`.

Considering only the users who have received at least a serious warning:

* A bar chart which indicates the number of users who have decreased their activity in the community within the time interval of the last serious warning received.
* The graph above but considering only men and women
* A bar chart which compares the percentage of women and men who have decreased their activity
* Considering the five users who have received the highest amount of edits:
    - A line chart which shows the user activity over months with some vertical lines, which indicate one or more warning.
    - A line chart illustrating the [`z-score`](https://en.wikipedia.org/wiki/Standard_score) of the user history within the time interval of the last serious user warning received

## Run

In order to call the scripts on all the MongoDB database collections, it is possibile to run the `run` bash script.

```bash
./run.sh
```

First of all, be sure you have modified all the readonly variables so as to fit your needs; feel free to change whatever you want.

The dependencies of the previously defined script are

* [GNU parallel](https://www.gnu.org/software/parallel/)

## Docker

So as to call the entire program in a [`Docker`](https://www.docker.com/) cotainer, a `Dockerfile` has been provided.

First, you need to change the content of the `run.sh` file in order to fill your requirements, such as the files' locations and which operation should be carried out by the script.

Then, you can build the Docker image by typing:

```bash
docker build -t warning-dropoff .
```

Then, make sure you have your local MongoDB instance working with all the required data.

Finally, run the docker image:

```bash
docker run --network="host" warning-dropoff
```