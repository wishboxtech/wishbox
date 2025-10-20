#!/bin/bash

set -o errexit
set -o nounset

celery -A src.core worker -l INFO