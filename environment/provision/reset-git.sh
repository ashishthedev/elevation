#!/bin/bash

echo '************************'
echo '***** reset-git.sh *****'
echo '************************'

set -euxo pipefail

rm -rdf /vagrant/.git
