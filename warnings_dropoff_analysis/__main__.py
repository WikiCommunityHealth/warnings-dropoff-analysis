import argparse
import os
from dotenv import load_dotenv
from .processors import user_warnings_metrics
from .utils import DatabaseService, writer

# Load config from a .env file:
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI') or None
OUTPUT_DIR = 'output'

def get_args() -> argparse.Namespace:
    """
    Gets the arguments from command line
    Returns:
        parsed_args argparse.Namespace: retrieved arguments
    """

    parser = argparse.ArgumentParser(
        prog='warnings_dropoff_analysis',
        description='Extract some metrics from the users\' activity in Wikipedia',
    )
    parser.add_argument(
        'database_name',
        metavar='DB',
        type=str,
        help='Name of the MongoDB database',
    )
    parser.add_argument(
        'collection',
        metavar='COLLECTION',
        type=str,
        help='Name of the MongoDB collection',
    )
    parser.add_argument(
        '--output-compression',
        choices={None, '7z', 'bz2', 'gzip'},
        required=False,
        default=None,
        help='Output compression format.',
    )

    subparsers = parser.add_subparsers(help='sub-commands help')
    user_warnings_metrics.configure_subparsers(subparsers)

    parsed_args = parser.parse_args()

    if 'func' not in parsed_args:
        parser.print_usage()
        parser.exit(1)

    return parsed_args

def main() -> None:
    """
    Main function of the warnings_dropoff_analysis module
    """

    # obtain the command line arguments
    args = get_args()

    # open the pymongo connection to the remote MongoDB database
    database_service = DatabaseService(
        connection_string=MONGODB_URI, 
        database_name=args.database_name, 
        collection_name=args.collection)

    # obtain writers
    features_output = writer.output_writer(
        path='{}/{}'.format(OUTPUT_DIR, (args.collection + '.features.json')),
        compression=args.output_compression,
    )
    stats_output = writer.output_writer(
        path='{}/{}'.format(OUTPUT_DIR, (args.collection + '.stats.json')),
        compression=args.output_compression,
    )

    print('Start to analyze: {}/{}'.format(args.database_name, args.collection))

    # call the mail function of the subparser
    args.func(
        args,
        database_service,
        features_output,
        stats_output
    )

    features_output.close()
    stats_output.close()

if __name__ == '__main__':
    main()