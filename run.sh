#!/bin/bash

readonly SEX_TSV_LOCATION="../sex_tsv_location/"
readonly LANGUAGES_LOCATION="../output_languages_refactored/"
readonly WIKIBREAKS_LOCATION="../output_wikibreaks_refactored/"
readonly USER_WARNINGS_LOCATION="../output_user_warning_refactored/"
readonly DATABASE_NAME="user_metrics"
declare -a LOADERS=( "loaders/add_languages.py" "loaders/add_sex.py" "loaders/add_user_warnings.py" "loaders/add_wikibreaks.py" )
declare -a COLLECTIONS=( "cawiki_users" "enwiki_users" "itwiki_users" "eswiki_users" )
declare -a LANG_CODES=( "ca" "en" "it" "es" )
declare -a PLOTTERS_FUNCTIONS=( "plotter/serious_warnings_stats.py" " plotter/serious_warnings_stats.py")

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

ln -s "${SEX_TSV_LOCATION}" "wiki_sex"
ln -s "${LANGUAGES_LOCATION}" "wiki_lang"
ln -s "${WIKIBREAKS_LOCATION}" "wiki_breaks"
ln -s "${USER_WARNINGS_LOCATION}" "wiki_warnings"

###########################
###     Load data       ###
###########################

parallel -j+0 --progress python3 {1} {2} ::: "${LOADERS[@]}" ::: "${LANG_CODES[@]}"

if [[ $? != 0 ]]; then
    echo "Failed to load the data"
    exit 1
fi

###########################
###     Datasets        ###
###########################

parallel -j+0 --progress make run PROGRAM_FLAGS='"${DATABASE_NAME} {} --output-compression gzip\" ::: "${COLLECTIONS[@]}"'

if [[ $? != 0 ]]; then
    echo "Failed to compute the datasets"
    exit 1
fi

###########################
###     Plots           ###
###########################

parallel -j+0 --progress make plot PLOTTER_ARGV="{1}" PLOTTER="{2}" ::: "${LANG_CODES[@]}" ::: "${PLOTTERS_FUNCTIONS[@]}"

if [[ $? != 0 ]]; then
    echo "Failed to carry out the plots"
    exit 1
fi

###########################
###     Empty folders   ###
###########################

empty_folder "wiki_lang"
empty_folder "wiki_sex"
empty_folder "wiki_warnings"
empty_folder "wiki_breaks"