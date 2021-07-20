# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# TODO: Import the os module
import os



# END TODO

# TODO: Get the GCLOUD_PROJECT environment variable
project_id = os.environ.get('GCLOUD_PROJECT')


# END TODO

from flask import current_app

# TODO: Import the datastore module from the google.cloud package
from google.cloud import datastore



# END TODO

# TODO: Create a Cloud Datastore client object
# The datastore client object requires the Project ID.
# Pass through the Project ID you looked up from the
# environment variable earlier

datastore_client = datastore.Client(project_id)


# END TODO

"""
Returns a list of question entities for a given quiz
- filter by quiz name, defaulting to gcp
- no paging
- add in the entity key as the id property 
- if redact is true, remove the correctAnswer property from each entity
"""
def list_entities(quiz='gcp', redact=True): 
    query = datastore_client.query(kind='Question')
    query.add_filter('quiz', '=', query)
    results = list(query.fetch())
    for result in results:
        result['id'] = result.key.id
    if redact:
        for result in results:
            del result['correctAnswer']
    return results


"""
Create and persist and entity for each question
The Datastore key is the equivalent of a primary key in a relational database.
There are two main ways of writing a key:
1. Specify the kind, and let Datastore generate a unique numeric id
2. Specify the kind and a unique string id
"""
def save_question(question):
    key = datastore_client.key('Question')
    q_entity = datastore.Entity(key = key)

    for q_prop, q_val in question.items():
        q_entity[q_prop] = q_val

    datastore_client.put(q_entity)

