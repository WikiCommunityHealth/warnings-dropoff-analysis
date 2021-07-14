#!/bin/bash

readonly SEX_TSV_LOCATION="../sex_tsv_location/"
readonly LANGUAGES_LOCATION="../output_languages_refactored/"
readonly WIKIBREAKS_LOCATION="../output_wikibreaks_refactored/"
readonly USER_WARNINGS_LOCATION="../output_user_warning_refactored/"
readonly DATABASE_NAME="user_metrics"
declare -a LOADERS=( "loaders/add_languages.py" "loaders/add_sex.py" "loaders/add_user_warnings.py" "loaders/add_wikibreaks.py" )
declare -a COLLECTIONS=( "cawiki_users" "enwiki_users" "itwiki_users" "eswiki_users" )
declare -a LANG_CODES=( "ca" "en" "it" "es" )
declare -a PLOTTERS_FUNCTIONS=( "plotter/serious_warnings_stats.py" "plotter/retired_stats.py")

# load data
load_data=0
# empty folder
clear_folder=0
# make plots
make_plots=0

create_folder() {
    mkdir -p $1
}

empty_folder() {
    rm -rf $1
}

# Create folders

create_folder "wiki_lang"
create_folder "wiki_sex"
create_folder "wiki_warnings"
create_folder "wiki_breaks"

if [ ${load_data} = 1 ] ; then
    ln -s "${SEX_TSV_LOCATION}" "wiki_sex"
    ln -s "${LANGUAGES_LOCATION}" "wiki_lang"
    ln -s "${WIKIBREAKS_LOCATION}" "wiki_breaks"
    ln -s "${USER_WARNINGS_LOCATION}" "wiki_warnings"
fi


###########################
###     Load data       ###
###########################

if [ ${load_data} = 1 ] ; then
    parallel -j+0 --progress poetry run python3 {1} {2} ::: "${LOADERS[@]}" ::: "${LANG_CODES[@]}"

    if [[ $? != 0 ]]; then
        echo "Failed to load the data"
        exit 1
    fi
fi

###########################
###     Datasets        ###
###########################

printf "%s\n" ${COLLECTIONS[@]} | xargs -i make run PROGRAM_FLAGS="${DATABASE_NAME} {} --output-compression gzip"

if [[ $? != 0 ]]; then
    echo "Failed to compute the datasets"
    exit 1
fi

###########################
###     Plots           ###
###########################

if [ ${make_plots} = 1 ] ; then
    parallel -j+0 --progress make plot PLOTTER_ARGV='"{1}"' PLOTTER='"{2}"' ::: "${LANG_CODES[@]}" ::: "${PLOTTERS_FUNCTIONS[@]}"

    if [[ $? != 0 ]]; then
        echo "Failed to carry out the plots"
        exit 1
    fi
fi


###########################
###     Empty folders   ###
###########################

if [ ${clear_folder} = 1 ] ; then
    empty_folder "wiki_lang"
    empty_folder "wiki_sex"
    empty_folder "wiki_warnings"
    empty_folder "wiki_breaks"
fi