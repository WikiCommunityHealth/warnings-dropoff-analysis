#!/usr/bin/env python3

from typing import Iterator, Mapping
from .. import DatabaseService, CollectionService
from ..extractors import retired_extractor
from datetime import datetime
import argparse
import io
import json


def extract_metrics(
        collection: CollectionService, 
        month_to_be_considered_retired: int,
        month_average_calculus: int,
        stats: Mapping) -> Iterator[None]:
    """
    Exdtract the metrics from users in drop-off

    Args:
        collection (CollectionService): user collection
        month_to_be_considered_retired (int): month to be considered in drop-off
        stats (Mapping): basic stats of the computations

    Yields:
        Iterator[UserMetrics]: user's in drop-off metrics
    """

    print('Current count of elements in the collection: {}'.format(collection.num_documents))
    counter = 0

    # filter the users: only those who have received some warnings
    for user in collection.service.find({'user_warnings_received': {"$exists": True }}):
        
        metrics, ambiguous = retired_extractor.extract_metrics(user, month_to_be_considered_retired, month_average_calculus)

        # interested only in retired users
        if metrics:
            counter += 1
            if counter % 10_000 == 0:
                print('I have done {} users so far'.format(counter))
            stats['drop_off']['users_dropoff'] += 1
            if metrics.retirement_declared:
                stats['drop_off']['retired_users'] += 1
            yield metrics
        elif ambiguous:
            stats['drop_off']['ambiguous_users'] += 1
        else:
            stats['drop_off']['not_drop_off'] += 1

        stats['performance']['user_analyzed'] += 1

    print('Total users in drop-off: {}'.format(counter))


def configure_subparsers(subparsers) -> None:
    """Configure a new subparser for the user warnings metrics extraction."""
    parser = subparsers.add_parser(
        'extract-user-warnings-metrics',
        help='Extract the user warnings metrics',
    )
    parser.add_argument(
        'month_to_be_considered_retired',
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        type=int,
        help='Number of month used to consider a user retired.',
    )
    parser.add_argument(
        'month_average_calculus',
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        type=int,
        help='Number of month used to perform the the average activity count calculus',
    )
    parser.set_defaults(func=main)

def main(
    args:  argparse.Namespace,
    database_service: DatabaseService,
    features_output_h: io.TextIOWrapper,
    stats_output_h: io.TextIOWrapper
) -> None:

    stats = {
        'performance': {
            'start_time': None,
            'end_time': None,
            'user_analyzed': 0
        },
        'drop_off': {
            'retired_users': 0,
            'users_dropoff': 0,
            'ambiguous_users': 0,
            'not_drop_off': 0
        }
    }

    stats['performance']['start_time'] = datetime.utcnow()

    metrics_generator = extract_metrics(
        database_service.collection, 
        args.month_to_be_considered_retired,
        args.month_average_calculus,
        stats)

    stats['performance']['start_time'] = datetime.utcnow()

    for obj in metrics_generator:
        features_output_h.write(obj.json)
        features_output_h.write("\n")
    
    stats['performance']['end_time'] = datetime.utcnow()
    stats_output_h.write(json.dumps(stats, indent=4, default=str))